import streamlit as st
from pathlib import Path
import google.generativeai as genai

from Api_Key import api_key
genai.configure(api_key = api_key)

generation_config = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k":32,
    "max_output_tokens": 4096
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]
prompts = {
    "English": """
   Given the picture provided, create a compelling and engaging story that aligns with the mood and tone of the image. The story should have the following characteristics:

For Joyful, Positive, or Neutral Images:

Create an exciting and joyful journey. Build a narrative that is full of adventure, optimism, and heartwarming moments.
Describe the characters, setting, and events in a way that captures the excitement, wonder, and positivity seen in the image.
Make sure the story feels like an inspiring journey, where the protagonist experiences growth, happiness, and moments of triumph.
For Scary, Eerie, or Unsettling Images:

Create a scary or eerie storyline that matches the atmosphere of the image. Develop a suspenseful and chilling narrative filled with tension and unexpected twists.
Focus on creating a sense of fear, mystery, and unease. Introduce elements of the supernatural, dark forces, or disturbing encounters that align with the visual cues in the image.
The story should gradually build suspense and keep the reader on edge, with an unsettling tone throughout.
In both cases, describe the environment in vivid detail, and provide background information to make the reader feel immersed in the scene. Ensure the narrative fits the mood of the image, whether it’s a joyful adventure or a thrilling horror tale.
    """,
    "Spanish": """
     Dada la imagen proporcionada, crea una historia cautivadora y atractiva que se alinee con el estado de ánimo y el tono de la imagen. La historia debe tener las siguientes características:

Para Imágenes Alegres, Positivas o Neutrales:

Crea un viaje emocionante y alegre. Construye una narrativa llena de aventura, optimismo y momentos conmovedores. Describe a los personajes, el escenario y los eventos de manera que capture la emoción, la maravilla y la positividad que se ven en la imagen. Asegúrate de que la historia se sienta como un viaje inspirador, donde el protagonista experimenta crecimiento, felicidad y momentos de triunfo.

Para Imágenes Escalofriantes, Misteriosas o Inquietantes:

Crea una historia aterradora o misteriosa que coincida con la atmósfera de la imagen. Desarrolla una narrativa llena de suspenso y escalofríos, llena de tensión y giros inesperados. Enfócate en crear una sensación de miedo, misterio e inquietud. Introduce elementos sobrenaturales, fuerzas oscuras o encuentros perturbadores que coincidan con las señales visuales de la imagen. La historia debe generar gradualmente suspenso y mantener al lector en tensión, con un tono inquietante a lo largo de toda la narración.

En ambos casos, describe el entorno con detalles vívidos y proporciona información de fondo para hacer que el lector se sienta inmerso en la escena. Asegúrate de que la narrativa se ajuste al estado de ánimo de la imagen, ya sea una aventura alegre o una aterradora historia de horror.""",
    
    "Turkish":"""Sağlanan resme göre, resmin ruh haline ve tonuna uygun, etkileyici ve ilgi çekici bir hikaye oluşturun. Hikayenin aşağıdaki özelliklere sahip olması gerekir:

Neşeli, Pozitif veya Nötr Resimler İçin:

Heyecan verici ve neşeli bir yolculuk yaratın. Macera, iyimserlik ve iç ısıtan anlarla dolu bir anlatı oluşturun. Karakterleri, ortamı ve olayları, resimde görülen heyecanı, hayreti ve pozitifliği yakalayacak şekilde tanımlayın. Hikayenin, ana karakterin büyüme, mutluluk ve zafer anları yaşadığı ilham verici bir yolculuk gibi hissettirdiğinden emin olun. TEKRARLAMALARDAN UZAK DURUN UZUN VE AKICI BİR HİKAYE OLSUN.

Korkunç, Garip veya Rahatsız Edici Resimler İçin:

Resmin atmosferine uygun korkutucu veya garip bir hikaye oluşturun. Gerilim ve soğuklukla dolu, beklenmedik dönüşlerle dolu bir anlatı geliştirin. Korku, gizem ve rahatsızlık hissi yaratmaya odaklanın. Görsel ipuçlarına uygun şekilde doğaüstü unsurlar, karanlık güçler veya rahatsız edici karşılaşmalar tanıtın. Hikaye, gerilim oluşturarak okuyucuyu kenarda tutmalı ve rahatsız edici bir tonla devam etmelidir. TEKRARLAMALARDAN UZAK DURUN UZUN VE AKICI BİR HİKAYE OLSUN.

Her iki durumda da, çevreyi canlı bir şekilde tanımlayın ve okuyucunun sahneye tamamen dahil hissetmesini sağlayacak arka plan bilgisi verin. Anlatının, resmin ruh haline uygun olduğundan emin olun, ister neşeli bir macera ister heyecan verici bir korku hikayesi olsun. """,
    "German":"""
 Basierend auf dem bereitgestellten Bild erstellen Sie eine fesselnde und ansprechende Geschichte, die mit der Stimmung und dem Ton des Bildes übereinstimmt. Die Geschichte sollte folgende Merkmale aufweisen:

Für fröhliche, positive oder neutrale Bilder:

Erstellen Sie eine aufregende und fröhliche Reise. Erbauen Sie eine Erzählung, die voller Abenteuer, Optimismus und herzerwärmender Momente ist. Beschreiben Sie die Charaktere, die Umgebung und die Ereignisse auf eine Weise, die die Aufregung, das Staunen und die Positivität des Bildes einfängt. Stellen Sie sicher, dass sich die Geschichte wie eine inspirierende Reise anfühlt, bei der der Protagonist Wachstum, Glück und Momente des Triumphs erlebt.

Für gruselige, unheimliche oder verstörende Bilder:

Erstellen Sie eine gruselige oder unheimliche Geschichte, die zur Atmosphäre des Bildes passt. Entwickeln Sie eine fesselnde Erzählung, die voller Spannung und unerwarteter Wendungen ist. Fokussieren Sie sich darauf, ein Gefühl von Angst, Geheimnis und Unbehagen zu erzeugen. Führen Sie übernatürliche Elemente, dunkle Kräfte oder verstörende Begegnungen ein, die mit den visuellen Hinweisen des Bildes übereinstimmen. Die Geschichte sollte allmählich Spannung aufbauen und den Leser in Atem halten, mit einem beunruhigenden Ton in der gesamten Erzählung.

In beiden Fällen beschreiben Sie die Umgebung lebendig und liefern Hintergrundinformationen, um den Leser in die Szene einzutauchen. Stellen Sie sicher, dass die Erzählung der Stimmung des Bildes entspricht, sei es ein fröhliches Abenteuer oder eine spannende Horror-Geschichte

""","Chinese":"""
根据提供的图片，创造一个引人入胜的故事，符合图片的情绪和氛围。故事应具有以下特点：

对于快乐、积极或中立的图像：

创造一个令人兴奋和愉快的旅程。构建一个充满冒险、乐观和温馨时刻的叙事。 以捕捉图像中所看到的兴奋、惊奇和积极性为方式描述人物、背景和事件。 确保故事让人感觉像是一场启发性的旅程，主人公在其中经历成长、幸福和胜利时刻。

对于可怕、神秘或不安的图像：

创造一个恐怖或神秘的故事情节，匹配图像的氛围。发展一个充满悬念和寒意的叙事，充满紧张和意外的转折。 专注于创造恐惧、神秘和不安的感觉。引入超自然元素、黑暗力量或令人不安的遭遇，符合图像中的视觉提示。 故事应逐渐建立悬念，并始终保持令人不安的氛围，使读者保持紧张。

在这两种情况下，都要用生动的细节描述环境，并提供背景信息，让读者感受到身临其境的感觉。确保叙事符合图像的情绪，无论是愉快的冒险还是刺激的恐怖故事。
""",
"French":"""
  Étant donné l'image fournie, créez une histoire captivante et engageante qui s'aligne avec l'ambiance et le ton de l'image. L'histoire doit avoir les caractéristiques suivantes :

Pour les Images Joyeuses, Positives ou Neutres :

Créez un voyage excitant et joyeux. Construisez un récit plein d'aventure, d'optimisme et de moments réconfortants. Décrivez les personnages, le décor et les événements de manière à capturer l'excitation, l'émerveillement et la positivité vus dans l'image. Assurez-vous que l'histoire semble être un voyage inspirant, où le protagoniste vit une croissance, du bonheur et des moments de triomphe.

Pour les Images Effrayantes, Étranges ou Inquiétantes :

Créez une histoire effrayante ou étrange qui correspond à l'atmosphère de l'image. Développez un récit captivant et glacé, rempli de tension et de rebondissements inattendus. Concentrez-vous sur la création d'un sentiment de peur, de mystère et d'inquiétude. Introduisez des éléments surnaturels, des forces sombres ou des rencontres perturbantes qui s'alignent avec les indices visuels de l'image. L'histoire devrait progressivement créer du suspense et garder le lecteur en haleine, avec un ton inquiétant tout au long du récit.

Dans les deux cas, décrivez l'environnement en détail et fournissez des informations contextuelles pour faire en sorte que le lecteur se sente immergé dans la scène. Assurez-vous que le récit correspond à l'ambiance de l'image, qu'il s'agisse d'une aventure joyeuse ou d'une histoire d'horreur palpitante.

""","Italian":"""
 Dato l'immagine fornita, crea una storia avvincente e coinvolgente che si allinei con l'umore e il tono dell'immagine. La storia dovrebbe avere le seguenti caratteristiche:

Per Immagini Gioiose, Positive o Neutre:

Crea un viaggio emozionante e gioioso. Costruisci una narrazione piena di avventura, ottimismo e momenti emozionanti. Descrivi i personaggi, l'ambientazione e gli eventi in modo da catturare l'entusiasmo, lo stupore e la positività che si vedono nell'immagine. Assicurati che la storia sembri un viaggio ispiratore, dove il protagonista vive momenti di crescita, felicità e trionfo.

Per Immagini Spaventose, Misteriose o Inquietanti:

Crea una trama spaventosa o misteriosa che corrisponda all'atmosfera dell'immagine. Sviluppa una narrazione carica di suspense e brivido, piena di tensione e colpi di scena inaspettati. Concentrati nel creare una sensazione di paura, mistero e disagio. Introduci elementi soprannaturali, forze oscure o incontri disturbanti che si allineano con i suggerimenti visivi nell'immagine. La storia dovrebbe gradualmente accumulare suspense e tenere il lettore sulle spine, con un tono inquietante durante tutto il racconto.

In entrambi i casi, descrivi l'ambiente con dettagli vividi e fornisci informazioni di contesto per far sentire il lettore immerso nella scena. Assicurati che la narrazione si adatti all'umore dell'immagine, che si tratti di un'avventura gioiosa o di una storia horror emozionante.
""","Russian":"""  вы играете важную роль в оценке медицинских изображений для престижной больницы. Ваш опыт жизненно важен.

Ваши ключевые обязанности включают:

- Глубокий анализ: Проведение тщательного обследования каждого изображения с акцентом на выявление любых аномальных находок.
- Отчет о находках: Документирование всех выявленных аномалий или признаков заболевания ясным и организованным образом.
- Следующие шаги и рекомендации: На основе ваших находок предложите потенциальные действия, включая дополнительные тесты или необходимые лечения.
- Предлагаемые лечения: При необходимости предоставьте рекомендации по возможным вариантам лечения или вмешательства.

Важные соображения:

- Ограничения ответа: Отвечайте только в том случае, если изображение связано с проблемами здоровья человека.
- Четкость изображения: Если качество изображения мешает четкому анализу, укажите, что некоторые детали «нельзя определить на основе предоставленного изображения».
- Отказ от ответственности: Включите заявление: «Проконсультируйтесь с врачом, прежде чем принимать решения».
- Ценность ваших выводов: Ваши выводы имеют критическое значение для информирования клинических решений. Пожалуйста, продолжайте анализ, следуя вышеуказанному структурированному формату, обеспечивая, чтобы ответ содержал не менее 150 слов.
- Пожалуйста, создайте ответ с выводом под следующими четырьмя заголовками: Подробный анализ, Отчет о находках, Рекомендации и следующие шаги, и Предложения по лечению.

"""
    
}

model = genai.GenerativeModel(model_name = "gemini-1.5-flash-002",
                              generation_config = generation_config,
                              safety_settings = safety_settings)

st.set_page_config(page_title = "FantasyFoundry", page_icon = "🪁")

st.markdown("<h1 style='text-align: center;'>🪐 FantasyFoundry 🪐</h1>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)

st.subheader("Upload an image to create your own story!")
language = st.selectbox("Select the language for the analysis:", list(prompts.keys()))

uploaded_file = st.file_uploader("Upload an image for story", 
                                 type = ["png","jpg","jpeg"])

if uploaded_file:
    st.image(uploaded_file, width = 650, caption="Uploaded Image")


submit_button = st.button("Generate the Story")

if submit_button:
    image_data = uploaded_file.getvalue()

    image_parts = [
        {
        "mime_type": uploaded_file.type,
        "data": image_data 
        }
    ]
    system_prompt = prompts[language]
    prompt_parts = [
        
        image_parts[0],
        system_prompt,
    ]
    st.header("Story is being created...")
    response = model.generate_content(prompt_parts)
    st.write(response.text)

