# install_argos_models.py

from argostranslate import package, translate
import logging

logger = logging.getLogger(__name__)

def install():
    logger.info("Checking & Installing Argos Translate models...")
    package.update_package_index()
    available_packages = package.get_available_packages()
    installed_languages = translate.get_installed_languages()

    required_directions = [("de", "en"), ("en", "de")]

    for from_code, to_code in required_directions:
        src_lang = next((lang for lang in installed_languages if lang.code == from_code), None)
        tgt_lang = next((lang for lang in installed_languages if lang.code == to_code), None)

        if not src_lang or not tgt_lang or not src_lang.get_translation(tgt_lang):
            logger.info(f"Installing Argos model for {from_code}->{to_code}...")
            pkg = next(p for p in available_packages if p.from_code == from_code and p.to_code == to_code)
            package.install_from_path(pkg.download())
        else:
            logger.info(f"Model already installed: {from_code} → {to_code}")
