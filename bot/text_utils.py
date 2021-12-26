import json
import os

from config import DATABASE_URL
from models import Text, db
from pathlib import Path


def load_translations(path: str = "src/translations") -> dict:
    texts = dict()
    translations_path = Path(__file__).parent.absolute() / path
    translation_files = os.listdir(translations_path)
    for filename in translation_files:
        language = filename.split('.')[0]
        with open(f'{translations_path}/{filename}', 'r') as f:
            data = json.loads(f.read())
            texts[language] = data

    return texts


def is_all_texts_exist(required_text_names: list, db_texts: list) -> bool:
    for required in required_text_names:
        found = False
        for text in db_texts:
            if required == text.name:
                found = True
                break

        if not found:
            return False

    return True


async def fill_db_texts_if_need(cached_texts: dict) -> bool:
    await db.set_bind(DATABASE_URL)

    db_texts = await db.all(Text.query)
    lang_code = list(cached_texts.keys())[0]
    required_text_names = list(cached_texts[lang_code].keys())

    if is_all_texts_exist(required_text_names, db_texts):
        return False

    await Text.__table__.gino.drop()
    await Text.__table__.gino.create()

    for language, texts in cached_texts.items():
        print('language', language, 'text', texts)
        for name, value in texts.items():
            await Text(name=name, value=value, language=language).create()

    await db.pop_bind().close()
    return True


async def set_cached_texts_from_db():
    await db.set_bind(DATABASE_URL)
    db_texts = await db.all(Text.query)
    await db.pop_bind().close()

    for text in db_texts:
        language = text.language
        if language not in cached_texts:
            cached_texts[language] = dict()

        cached_texts[language][text.name] = text.value


cached_texts = load_translations()


def _(text_name, lang_code='ru'):
    return cached_texts[lang_code][text_name]
