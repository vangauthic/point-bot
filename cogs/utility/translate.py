import discord
import yaml
import translators as ts
from langdetect import detect
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = discord.Color.from_str(data['DefaultStyles']['EMBED_COLOR'])

language_codes = [
    'af',  # Afrikaans
    'sq',  # Albanian
    'am',  # Amharic
    'ar',  # Arabic
    'hy',  # Armenian
    'az',  # Azerbaijani
    'eu',  # Basque
    'be',  # Belarusian
    'bn',  # Bengali
    'bs',  # Bosnian
    'bg',  # Bulgarian
    'ca',  # Catalan
    'ceb', # Cebuano
    'zh',  # Chinese
    'hr',  # Croatian
    'cs',  # Czech
    'da',  # Danish
    'nl',  # Dutch
    'en',  # English
    'eo',  # Esperanto
    'et',  # Estonian
    'fi',  # Finnish
    'fr',  # French
    'gl',  # Galician
    'ka',  # Georgian
    'de',  # German
    'el',  # Greek
    'gu',  # Gujarati
    'ht',  # Haitian Creole
    'ha',  # Hausa
    'haw', # Hawaiian
    'he',  # Hebrew
    'hi',  # Hindi
    'hmn', # Hmong
    'hu',  # Hungarian
    'is',  # Icelandic
    'ig',  # Igbo
    'id',  # Indonesian
    'ga',  # Irish
    'it',  # Italian
    'ja',  # Japanese
    'jw',  # Javanese
    'kn',  # Kannada
    'kk',  # Kazakh
    'km',  # Khmer
    'rw',  # Kinyarwanda
    'ko',  # Korean
    'ku',  # Kurdish (Kurmanji)
    'ky',  # Kyrgyz
    'lo',  # Lao
    'la',  # Latin
    'lv',  # Latvian
    'lt',  # Lithuanian
    'lb',  # Luxembourgish
    'mk',  # Macedonian
    'mg',  # Malagasy
    'ms',  # Malay
    'ml',  # Malayalam
    'mt',  # Maltese
    'mi',  # Maori
    'mr',  # Marathi
    'mn',  # Mongolian
    'my',  # Myanmar (Burmese)
    'ne',  # Nepali
    'no',  # Norwegian
    'ny',  # Nyanja (Chichewa)
    'or',  # Odia (Oriya)
    'ps',  # Pashto
    'fa',  # Persian
    'pl',  # Polish
    'pt',  # Portuguese
    'pa',  # Punjabi
    'ro',  # Romanian
    'ru',  # Russian
    'sm',  # Samoan
    'gd',  # Scots Gaelic
    'sr',  # Serbian
    'st',  # Sesotho
    'sn',  # Shona
    'sd',  # Sindhi
    'si',  # Sinhala
    'sk',  # Slovak
    'sl',  # Slovenian
    'so',  # Somali
    'es',  # Spanish
    'su',  # Sundanese
    'sw',  # Swahili
    'sv',  # Swedish
    'tg',  # Tajik
    'ta',  # Tamil
    'tt',  # Tatar
    'te',  # Telugu
    'th',  # Thai
    'tr',  # Turkish
    'tk',  # Turkmen
    'uk',  # Ukrainian
    'ur',  # Urdu
    'ug',  # Uyghur
    'uz',  # Uzbek
    'vi',  # Vietnamese
    'cy',  # Welsh
    'xh',  # Xhosa
    'yi',  # Yiddish
    'yo',  # Yoruba
    'zu'   # Zulu
]

flag_emoji_dict = {
    'af': '🇿🇦',  # Afrikaans (South Africa)
    'sq': '🇦🇱',  # Albanian (Albania)
    'am': '🇪🇹',  # Amharic (Ethiopia)
    'ar': '🇸🇦',  # Arabic (Saudi Arabia)
    'hy': '🇦🇲',  # Armenian (Armenia)
    'az': '🇦🇿',  # Azerbaijani (Azerbaijan)
    'eu': '🇪🇸',  # Basque (Spain)
    'be': '🇧🇾',  # Belarusian (Belarus)
    'bn': '🇧🇩',  # Bengali (Bangladesh)
    'bs': '🇧🇦',  # Bosnian (Bosnia and Herzegovina)
    'bg': '🇧🇬',  # Bulgarian (Bulgaria)
    'ca': '🇪🇸',  # Catalan (Spain)
    'ceb': '🇵🇭', # Cebuano (Philippines)
    'zh': '🇨🇳',  # Chinese (China)
    'hr': '🇭🇷',  # Croatian (Croatia)
    'cs': '🇨🇿',  # Czech (Czech Republic)
    'da': '🇩🇰',  # Danish (Denmark)
    'nl': '🇳🇱',  # Dutch (Netherlands)
    'en': '🇺🇸',  # English (USA)
    'eo': '🌍',   # Esperanto (World)
    'et': '🇪🇪',  # Estonian (Estonia)
    'fi': '🇫🇮',  # Finnish (Finland)
    'fr': '🇫🇷',  # French (France)
    'gl': '🇪🇸',  # Galician (Spain)
    'ka': '🇬🇪',  # Georgian (Georgia)
    'de': '🇩🇪',  # German (Germany)
    'el': '🇬🇷',  # Greek (Greece)
    'gu': '🇮🇳',  # Gujarati (India)
    'ht': '🇭🇹',  # Haitian Creole (Haiti)
    'ha': '🇳🇬',  # Hausa (Nigeria)
    'haw': '🇺🇸', # Hawaiian (USA)
    'he': '🇮🇱',  # Hebrew (Israel)
    'hi': '🇮🇳',  # Hindi (India)
    'hmn': '🇱🇦', # Hmong (Laos)
    'hu': '🇭🇺',  # Hungarian (Hungary)
    'is': '🇮🇸',  # Icelandic (Iceland)
    'ig': '🇳🇬',  # Igbo (Nigeria)
    'id': '🇮🇩',  # Indonesian (Indonesia)
    'ga': '🇮🇪',  # Irish (Ireland)
    'it': '🇮🇹',  # Italian (Italy)
    'ja': '🇯🇵',  # Japanese (Japan)
    'jw': '🇮🇩',  # Javanese (Indonesia)
    'kn': '🇮🇳',  # Kannada (India)
    'kk': '🇰🇿',  # Kazakh (Kazakhstan)
    'km': '🇰🇭',  # Khmer (Cambodia)
    'rw': '🇷🇼',  # Kinyarwanda (Rwanda)
    'ko': '🇰🇷',  # Korean (South Korea)
    'ku': '🇮🇶',  # Kurdish (Kurmanji) (Iraq)
    'ky': '🇰🇬',  # Kyrgyz (Kyrgyzstan)
    'lo': '🇱🇦',  # Lao (Laos)
    'la': '🇻🇦',  # Latin (Vatican)
    'lv': '🇱🇻',  # Latvian (Latvia)
    'lt': '🇱🇹',  # Lithuanian (Lithuania)
    'lb': '🇱🇺',  # Luxembourgish (Luxembourg)
    'mk': '🇲🇰',  # Macedonian (North Macedonia)
    'mg': '🇲🇬',  # Malagasy (Madagascar)
    'ms': '🇲🇾',  # Malay (Malaysia)
    'ml': '🇮🇳',  # Malayalam (India)
    'mt': '🇲🇹',  # Maltese (Malta)
    'mi': '🇳🇿',  # Maori (New Zealand)
    'mr': '🇮🇳',  # Marathi (India)
    'mn': '🇲🇳',  # Mongolian (Mongolia)
    'my': '🇲🇲',  # Myanmar (Burma)
    'ne': '🇳🇵',  # Nepali (Nepal)
    'no': '🇳🇴',  # Norwegian (Norway)
    'ny': '🇲🇼',  # Nyanja (Chichewa) (Malawi)
    'or': '🇮🇳',  # Odia (Oriya) (India)
    'ps': '🇦🇫',  # Pashto (Afghanistan)
    'fa': '🇮🇷',  # Persian (Iran)
    'pl': '🇵🇱',  # Polish (Poland)
    'pt': '🇵🇹',  # Portuguese (Portugal)
    'pa': '🇮🇳',  # Punjabi (India)
    'ro': '🇷🇴',  # Romanian (Romania)
    'ru': '🇷🇺',  # Russian (Russia)
    'sm': '🇼🇸',  # Samoan (Samoa)
    'gd': '🏴', # Scots Gaelic (Scotland)
    'sr': '🇷🇸',  # Serbian (Serbia)
    'st': '🇱🇸',  # Sesotho (Lesotho)
    'sn': '🇿🇼',  # Shona (Zimbabwe)
    'sd': '🇵🇰',  # Sindhi (Pakistan)
    'si': '🇱🇰',  # Sinhala (Sri Lanka)
    'sk': '🇸🇰',  # Slovak (Slovakia)
    'sl': '🇸🇮',  # Slovenian (Slovenia)
    'so': '🇸🇴',  # Somali (Somalia)
    'es': '🇪🇸',  # Spanish (Spain)
    'su': '🇮🇩',  # Sundanese (Indonesia)
    'sw': '🇰🇪',  # Swahili (Kenya)
    'sv': '🇸🇪',  # Swedish (Sweden)
    'tg': '🇹🇯',  # Tajik (Tajikistan)
    'ta': '🇮🇳',  # Tamil (India)
    'tt': '🇷🇺',  # Tatar (Russia)
    'te': '🇮🇳',  # Telugu (India)
    'th': '🇹🇭',  # Thai (Thailand)
    'tr': '🇹🇷',  # Turkish (Turkey)
    'tk': '🇹🇲',  # Turkmen (Turkmenistan)
    'uk': '🇺🇦',  # Ukrainian (Ukraine)
    'ur': '🇵🇰',  # Urdu (Pakistan)
    'ug': '🇨🇳',  # Uyghur (China)
    'uz': '🇺🇿',  # Uzbek (Uzbekistan)
    'vi': '🇻🇳',  # Vietnamese (Vietnam)
    'cy': '🏴', # Welsh (Wales)
    'xh': '🇿🇦',  # Xhosa (South Africa)
    'yi': '🇮🇱',  # Yiddish (Israel)
    'yo': '🇳🇬',  # Yoruba (Nigeria)
    'zu': '🇿🇦'   # Zulu (South Africa)
}

long_form_dict = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'zh': 'Chinese',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'rw': 'Kinyarwanda',
    'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'ny': 'Nyanja (Chichewa)',
    'or': 'Odia (Oriya)',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'tt': 'Tatar',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'tk': 'Turkmen',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'
}


class TranslateModal(discord.ui.Modal, title='Translate'):
    def __init__(self, bot: commands.Bot, message: discord.Message):
        super().__init__(timeout=None)
        self.bot = bot
        self.message = message

    language = discord.ui.TextInput(
        label="What language would you like to translate to?",
        placeholder='en, de, fr, es, ru...',
        max_length=120,
        style=discord.TextStyle.short,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        to_lang = self.language.value.lower()
        if to_lang in language_codes:
            translated_text = ts.translate_text(query_text=self.message.content, to_language=to_lang)
            from_lang = detect(self.message.content)
            first_flag = flag_emoji_dict.get(from_lang)
            second_flag = flag_emoji_dict.get(to_lang)
            from_lang_long = long_form_dict.get(from_lang)
            to_lang_long = long_form_dict.get(to_lang)

            description = f"""
**{from_lang_long} {first_flag} (Auto-Detected):**
{self.message.content}

**{to_lang_long} {second_flag}**
{translated_text}
"""
            embed = discord.Embed(description=description, color=embed_color)
            embed.set_author(name=self.message.author.name, icon_url=self.message.author.display_avatar.url)
            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(description=f"{self.language.value.lower()} is not a valid language!", color=discord.Color.red())
            await interaction.followup.send(embed=embed, ephemeral=True)

class TranslateCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Translate',
            callback=self.translate,
        )
        self.bot.tree.add_command(self.ctx_menu)
        super().__init__()

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def translate(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.send_modal(TranslateModal(self.bot, message))

async def setup(bot):
    await bot.add_cog(TranslateCog(bot))