
import time
import os
import json
import logging
import requests
import pandas as pd

BASE_URL = "https://steamspy.com/api.php"

FICHIER_BRUT = "gamescope_catalogue_brut.csv"
FICHIER_SORTIE = "gamescope_catalogue_enrichi.csv"
FICHIER_ERREURS = "gamescope_erreurs.log"

TAILLE_PAUSE = 1.2
SAUVEGARDE_TOUTES_LES = 25

logging.basicConfig(
    filename=FICHIER_ERREURS,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

session = requests.Session()


def appeler_api(params):
    """Appelle SteamSpy avec quelques tentatives en cas d'erreur."""
    for tentative in range(4):
        try:
            reponse = session.get(
                BASE_URL,
                params=params,
                timeout=30
            )

            if reponse.status_code == 429:
                attente = int(reponse.headers.get("Retry-After", 10))
                time.sleep(attente)
                continue

            reponse.raise_for_status()
            donnees = reponse.json()

            if not isinstance(donnees, dict):
                raise ValueError("Réponse API inattendue.")

            return donnees

        except (requests.RequestException, ValueError) as erreur:
            logging.error(
                "Paramètres %s - tentative %s : %s",
                params, tentative + 1, erreur
            )
            if tentative < 3:
                time.sleep(2 ** tentative)

    return None


def recuperer_catalogue():
    """Récupère les deux pages de 1 000 jeux."""
    pages = []

    for page in [0, 1]:
        print(f"Récupération de la page {page}...")
        donnees = appeler_api({
            "request": "all",
            "page": page
        })

        if donnees is None:
            raise RuntimeError(
                f"Impossible de récupérer la page {page}. "
                "Relance le script plus tard."
            )

        df = pd.DataFrame.from_dict(donnees, orient="index")

        if "appid" not in df.columns:
            df["appid"] = df.index

        df["appid"] = pd.to_numeric(
            df["appid"], errors="coerce"
        )
        df = df.dropna(subset=["appid"])
        df["appid"] = df["appid"].astype(int)

        pages.append(df)
        print(f"{len(df)} jeux récupérés.")

        # SteamSpy recommande une pause importante pour request=all.
        if page == 0:
            time.sleep(65)

    catalogue = pd.concat(pages, ignore_index=True)
    catalogue = catalogue.drop_duplicates(
        subset="appid"
    ).reset_index(drop=True)

    catalogue.to_csv(
        FICHIER_BRUT,
        index=False,
        encoding="utf-8-sig"
    )

    return catalogue


def main():
    if os.path.exists(FICHIER_BRUT):
        print("Catalogue brut existant : chargement du fichier.")
        jeux = pd.read_csv(FICHIER_BRUT)
    else:
        jeux = recuperer_catalogue()

    jeux["appid"] = pd.to_numeric(
        jeux["appid"], errors="coerce"
    )
    jeux = jeux.dropna(subset=["appid"])
    jeux["appid"] = jeux["appid"].astype(int)
    jeux = jeux.drop_duplicates(subset="appid")

    if os.path.exists(FICHIER_SORTIE):
        enrichi = pd.read_csv(FICHIER_SORTIE)
        deja_traites = set(
            pd.to_numeric(
                enrichi["appid"], errors="coerce"
            ).dropna().astype(int)
        )
        resultats = enrichi.to_dict("records")
    else:
        deja_traites = set()
        resultats = []

    print(f"Catalogue : {len(jeux)} jeux.")
    print(f"Déjà traités : {len(deja_traites)}.")

    nouveaux = 0

    for position, (_, jeu) in enumerate(
        jeux.iterrows(), start=1
    ):
        appid = int(jeu["appid"])

        if appid in deja_traites:
            continue

        details = appeler_api({
            "request": "appdetails",
            "appid": appid
        })

        ligne = jeu.to_dict()

        if details is None:
            ligne["genre"] = None
            ligne["tags"] = None
            ligne["statut_collecte"] = "erreur"
            logging.error("Échec définitif pour appid=%s", appid)
        else:
            ligne["genre"] = details.get("genre")
            ligne["tags"] = json.dumps(
                details.get("tags"),
                ensure_ascii=False
            )
            ligne["statut_collecte"] = "ok"

        resultats.append(ligne)
        deja_traites.add(appid)
        nouveaux += 1

        if nouveaux % SAUVEGARDE_TOUTES_LES == 0:
            pd.DataFrame(resultats).to_csv(
                FICHIER_SORTIE,
                index=False,
                encoding="utf-8-sig"
            )
            print(
                f"Progression : {len(deja_traites)} "
                f"jeux traités sur {len(jeux)}."
            )

        time.sleep(TAILLE_PAUSE)

    pd.DataFrame(resultats).to_csv(
        FICHIER_SORTIE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nCollecte terminée.")
    print(f"Fichier enrichi : {FICHIER_SORTIE}")
    print(f"Journal des erreurs : {FICHIER_ERREURS}")


if __name__ == "__main__":
    main()
