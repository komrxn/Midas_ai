"""i18n Translation Engine for Midas Bot."""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class Translator:
    """Translation engine with semantic keys and interpolation."""
    
    def __init__(self, locales_dir: str = "bot/locales"):
        self.locales_dir = Path(locales_dir)
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.load_translations()
    
    def load_translations(self):
        """Load all translation files for all languages."""
        for lang_dir in self.locales_dir.iterdir():
            if not lang_dir.is_dir():
                continue
                
            lang = lang_dir.name
            self.translations[lang] = {}
            
            # Load all JSON files in language directory
            for json_file in lang_dir.glob("*.json"):
                namespace = json_file.stem  # e.g., 'common', 'auth', 'transactions'
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.translations[lang][namespace] = data
                        logger.info(f"Loaded {lang}/{namespace}.json")
                except Exception as e:
                    logger.error(f"Failed to load {json_file}: {e}")
    
    def t(self, key: str, lang: str = 'uz', **kwargs) -> str:
        """
        Translate a key with optional interpolation.
        
        Args:
            key: Dot-notation key (e.g., "transaction.fields.amount")
            lang: Language code (uz, ru, en)
            **kwargs: Variables for interpolation
            
        Returns:
            Translated string with interpolation applied
            
        Examples:
            t("auth.registration.welcome", lang="uz", name="Zahir")
            t("transaction.display.amount", lang="ru", currency="UZS", amount=50000)
        """
        # Fallback chain: requested lang → uz → en → key itself
        result = self._get_translation(key, lang)
        
        if result is None:
            result = self._get_translation(key, 'uz')
        
        if result is None:
            result = self._get_translation(key, 'en')
        
        if result is None:
            logger.warning(f"Missing translation: {key} (lang: {lang})")
            return key
        
        # Apply interpolation
        if kwargs:
            try:
                # Support both {{variable}} and {variable} syntax
                for var, value in kwargs.items():
                    result = result.replace(f"{{{{{var}}}}}", str(value))
                    result = result.replace(f"{{{var}}}", str(value))
            except Exception as e:
                logger.error(f"Interpolation error for key '{key}': {e}")
        
        return result
    
    def _get_translation(self, key: str, lang: str) -> Optional[str]:
        """Get translation for a specific language."""
        if lang not in self.translations:
            return None
        
        # Split key: "transaction.fields.amount" → ["transaction", "fields", "amount"]
        parts = key.split('.')
        
        if len(parts) < 2:
            return None
        
        namespace = parts[0]  # e.g., "transaction"
        path = parts[1:]      # e.g., ["fields", "amount"]
        
        if namespace not in self.translations[lang]:
            return None
        
        # Navigate nested dictionary
        current = self.translations[lang][namespace]
        for part in path:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        
        return current if isinstance(current, str) else None
    
    def translate_category(self, category_slug: str, lang: str = 'uz') -> str:
        """
        Translate category slug to localized name.
        
        Args:
            category_slug: Category slug (e.g., "food", "transport")
            lang: Language code
            
        Returns:
            Localized category name or title-cased slug if no translation
        """
        translation = self.t(f"categories.{category_slug}", lang)
        
        # If translation is the key itself (not found), return title-cased slug
        if translation == f"categories.{category_slug}":
            return category_slug.replace('_', ' ').title()
        
        return translation


# Global translator instance
translator = Translator()


def t(key: str, lang: str = 'uz', **kwargs) -> str:
    """Shorthand for translator.t()"""
    return translator.t(key, lang, **kwargs)


def translate_category(category_slug: str, lang: str = 'uz') -> str:
    """Shorthand for translator.translate_category()"""
    return translator.translate_category(category_slug, lang)
