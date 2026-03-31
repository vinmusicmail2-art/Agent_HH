from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Optional

app = FastAPI(title="HH Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HH_API_URL = "https://api.hh.ru"

CATEGORIES = [
    # ── Раздел 1: AI-специалисты по видео ──
    {
        "id": "sec_ai_video", "type": "section",
        "name": "AI-специалисты по видео", "icon": "🤖"
    },
    {
        "id": "ai_creator", "type": "job",
        "name": "AI-креатор",
        "icon": "🎬",
        "query": "AI-креатор OR AI креатор OR AI video creator OR нейросети видео"
    },
    {
        "id": "ai_artist", "type": "job",
        "name": "AI-художник",
        "icon": "🎨",
        "query": "AI художник OR AI-художник OR Midjourney OR Stable Diffusion OR нейросети изображения"
    },
    {
        "id": "ai_videomaker", "type": "job",
        "name": "AI-видеомейкер",
        "icon": "🎥",
        "query": "AI-видеомейкер OR AI видеомейкер OR нейросети видео монтаж OR Runway Kling Luma"
    },
    {
        "id": "ai_video_content", "type": "job",
        "name": "Специалист по AI-видеоконтенту",
        "icon": "📱",
        "query": "специалист AI видеоконтент OR создание AI видео OR нейросети видеоконтент"
    },
    {
        "id": "ai_gen_video", "type": "job",
        "name": "Специалист по генерации видео (нейросети)",
        "icon": "⚡",
        "query": "генерация видео нейросети OR Runway Gen OR Kling OR Luma Dream Machine OR специалист нейросети видео"
    },
    {
        "id": "ai_factory", "type": "job",
        "name": "AI Factory специалист",
        "icon": "🏭",
        "query": "AI Factory OR ComfyUI автоматизация видео OR пайплайн нейросети видео OR массовая генерация видео"
    },
    {
        "id": "content_maker_ai", "type": "job",
        "name": "Контент-мейкер (AI video)",
        "icon": "✨",
        "query": "контент-мейкер нейросети OR контент мейкер AI OR видеоконтент нейросети соцсети"
    },
    {
        "id": "editor_ai", "type": "job",
        "name": "Видеомонтажер с нейросетями",
        "icon": "🖥️",
        "query": "видеомонтажер нейросети OR монтажер AI инструменты OR монтаж нейросети Topaz"
    },
    {
        "id": "ai_artist_anim", "type": "job",
        "name": "AI artist (видео / анимация)",
        "icon": "🌀",
        "query": "AI artist видео OR AI artist анимация OR AnimateDiff OR нейросети анимация"
    },
    {
        "id": "creator_ai", "type": "job",
        "name": "Креатор видеоконтента (нейросети)",
        "icon": "💡",
        "query": "креатор видеоконтент нейросети OR видеоконтент ИИ OR CapCut нейросети"
    },
    {
        "id": "ai_animation", "type": "job",
        "name": "Специалист по AI-анимации",
        "icon": "🎭",
        "query": "специалист AI анимация OR AI-анимация OR AnimateDiff Runway анимация OR Pika анимация"
    },
    {
        "id": "ai_production", "type": "job",
        "name": "Видеопродакшн с ИИ",
        "icon": "🎞️",
        "query": "видеопродакшн ИИ OR продакшн нейросети OR AI видео продакшн руководитель"
    },

    # ── Раздел 2: Режиссура и монтаж ──
    {
        "id": "sec_editing", "type": "section",
        "name": "Режиссура и монтаж", "icon": "🎬"
    },
    {
        "id": "edit_director", "type": "job",
        "name": "Режиссер монтажа",
        "icon": "🎞️",
        "query": "режиссер монтажа OR режиссёр монтажа"
    },
    {
        "id": "edit_director_promo", "type": "job",
        "name": "Режиссер монтажа (промо)",
        "icon": "📺",
        "query": "режиссер монтажа промо OR монтаж промо трейлер тизер"
    },
    {
        "id": "edit_director_news", "type": "job",
        "name": "Режиссер монтажа (новости)",
        "icon": "📰",
        "query": "режиссер монтажа новости OR монтаж новостных сюжетов OR Avid монтаж"
    },
    {
        "id": "videoeditor", "type": "job",
        "name": "Видеомонтажер",
        "icon": "✂️",
        "query": "видеомонтажер OR видео монтажер OR монтажер Premiere Pro DaVinci"
    },
    {
        "id": "editor_tech", "type": "job",
        "name": "Монтажер",
        "icon": "🔧",
        "query": "монтажер видео OR технический монтажер OR монтаж хроника"
    },
    {
        "id": "videographer_editor", "type": "job",
        "name": "Видеограф-монтажер",
        "icon": "📷",
        "query": "видеограф монтажер OR видеограф-монтажер OR съемка монтаж"
    },
    {
        "id": "operator_editor", "type": "job",
        "name": "Оператор-монтажер",
        "icon": "🎦",
        "query": "оператор-монтажер OR оператор монтажер OR съемка монтаж Sony Canon Blackmagic"
    },
    {
        "id": "edit_director2", "type": "job",
        "name": "Режиссер видеомонтажа",
        "icon": "🎬",
        "query": "режиссер видеомонтажа OR руководство монтажом видеопроекта"
    },
    {
        "id": "lead_editor", "type": "job",
        "name": "Ведущий режиссер монтажа",
        "icon": "👑",
        "query": "ведущий режиссер монтажа OR старший монтажер OR руководитель монтажа"
    },
    {
        "id": "asst_editor", "type": "job",
        "name": "Ассистент режиссера монтажа",
        "icon": "📋",
        "query": "ассистент режиссера монтажа OR ассистент монтажа OR помощник монтажера"
    },
    {
        "id": "postprod_head", "type": "job",
        "name": "Руководитель постпродакшна",
        "icon": "🏆",
        "query": "руководитель постпродакшна OR head of post-production OR руководитель постпроизводства"
    },

    # ── Раздел 3: Операторская работа ──
    {
        "id": "sec_camera", "type": "section",
        "name": "Операторская работа и съемка", "icon": "📷"
    },
    {
        "id": "camera_op", "type": "job",
        "name": "Оператор видеозаписи",
        "icon": "🎥",
        "query": "оператор видеозаписи OR видеооператор OR оператор Sony FX Canon RED ARRI"
    },
    {
        "id": "videographer", "type": "job",
        "name": "Видеограф",
        "icon": "🤳",
        "query": "видеограф OR videographer OR съемка мероприятий корпоративных видео"
    },
    {
        "id": "correspondent", "type": "job",
        "name": "Корреспондент (видеомонтаж)",
        "icon": "🎤",
        "query": "корреспондент видеомонтаж OR тележурналист OR журналист видеосюжет"
    },
    {
        "id": "tv_journalist", "type": "job",
        "name": "Тележурналист",
        "icon": "📡",
        "query": "тележурналист OR телевизионный журналист OR TV журналист"
    },

    # ── Раздел 4: Постпродакшн и моушн-дизайн ──
    {
        "id": "sec_postprod", "type": "section",
        "name": "Постпродакшн и моушн-дизайн", "icon": "🎨"
    },
    {
        "id": "colorist", "type": "job",
        "name": "Цветокорректор",
        "icon": "🌈",
        "query": "цветокорректор OR колорист OR цветокоррекция DaVinci Resolve OR colorist"
    },
    {
        "id": "postprod_spec", "type": "job",
        "name": "Специалист по постпродакшну",
        "icon": "⚙️",
        "query": "специалист постпродакшн OR постпродакшн специалист OR VFX монтаж цветокоррекция"
    },

    # ── Раздел 5: Звук ──
    {
        "id": "sec_sound", "type": "section",
        "name": "Звукозапись и сведение", "icon": "🎵"
    },
    {
        "id": "sound_director", "type": "job",
        "name": "Звукорежиссер",
        "icon": "🎚️",
        "query": "звукорежиссер OR звукорежиссёр OR audio engineer OR сведение мастеринг"
    },
    {
        "id": "sound_postprod", "type": "job",
        "name": "Звукорежиссер пост-продакшн",
        "icon": "🎛️",
        "query": "звукорежиссер постпродакшн OR озвучивание видео OR ADR шумоочистка"
    },
    {
        "id": "sound_producer", "type": "job",
        "name": "Саунд-продюсер",
        "icon": "🎼",
        "query": "саунд продюсер OR sound producer OR музыкальный продюсер видео"
    },
    {
        "id": "mastering", "type": "job",
        "name": "Мастеринг-инженер",
        "icon": "🔊",
        "query": "мастеринг инженер OR mastering engineer OR нормализация громкости LUFS"
    },
    {
        "id": "mixing", "type": "job",
        "name": "Специалист по сведению",
        "icon": "🎹",
        "query": "специалист сведение мастеринг OR mixing mastering OR аудио постпродакшн"
    },

    # ── Раздел 6: Контент и диджитал ──
    {
        "id": "sec_content", "type": "section",
        "name": "Контент и диджитал", "icon": "📲"
    },
    {
        "id": "content_maker", "type": "job",
        "name": "Контент-мейкер",
        "icon": "📝",
        "query": "контент-мейкер OR контент мейкер OR создание контента соцсети видео"
    },
    {
        "id": "smm_content", "type": "job",
        "name": "SMM-менеджер / Контент-мейкер",
        "icon": "📣",
        "query": "SMM менеджер контент-мейкер OR SMM видеоконтент OR ведение соцсетей видео"
    },
    {
        "id": "reelsmaker", "type": "job",
        "name": "Рилсмейкер",
        "icon": "📸",
        "query": "рилсмейкер OR reels maker OR Reels TikTok Shorts монтажер OR вертикальное видео"
    },

    # ── Раздел 7: Вайбкодинг ──
    {
        "id": "sec_vibe", "type": "section",
        "name": "Вайбкодинг / AI-разработка", "icon": "🌊"
    },
    {
        "id": "vibe_coder", "type": "job",
        "name": "Вайбкодер / Vibe Coder",
        "icon": "🌊",
        "query": "вайбкодер OR вайб-кодер OR вайбкодинг OR \"vibe coder\" OR \"vibe coding\" OR \"vibe developer\" OR \"vibe coding engineer\" OR \"vibe programmer\" OR \"vibe coder engineer\" OR \"vibe coder developer\" OR \"AI-native coder\" OR \"AI-first coder\" OR вайб-разработчик OR вайб-программист OR вайб-инженер OR \"vibe coder specialist\" OR \"vibe coding specialist\""
    },

    # ── Раздел 8: Смежные профессии ──
    {
        "id": "sec_related", "type": "section",
        "name": "Смежные профессии", "icon": "🔗"
    },
    {
        "id": "photographer", "type": "job",
        "name": "Фотограф (видеопроекты)",
        "icon": "📸",
        "query": "фотограф видеопроект OR фотограф продакшн OR фотограф Lightroom Photoshop"
    },
    {
        "id": "drone_op", "type": "job",
        "name": "Оператор дрона",
        "icon": "🚁",
        "query": "оператор дрона OR дрон-оператор OR квадрокоптер DJI аэросъемка"
    },
    {
        "id": "targetolog", "type": "job",
        "name": "Таргетолог (видеокреативы)",
        "icon": "🎯",
        "query": "таргетолог видеокреативы OR таргетолог видео реклама OR таргетированная реклама видео"
    },
]


@app.get("/api/categories")
def get_categories():
    return CATEGORIES


@app.get("/api/search")
async def search_jobs(
    query: str = Query(...),
    area: Optional[str] = Query(None),
    salary_from: Optional[int] = Query(None),
    experience: Optional[str] = Query(None),
    page: int = Query(0),
    per_page: int = Query(20),
):
    params = {
        "text": query,
        "page": page,
        "per_page": min(per_page, 100),
        "order_by": "relevance",
    }
    if area:
        params["area"] = area
    if salary_from:
        params["salary"] = salary_from
        params["only_with_salary"] = "true"
    if experience:
        params["experience"] = experience

    headers = {
        "User-Agent": "HH-Agent/1.0 (job search application)",
        "HH-User-Agent": "HH-Agent/1.0 (job search application)",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                f"{HH_API_URL}/vacancies",
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        items = []
        for v in data.get("items", []):
            salary = v.get("salary")
            salary_text = "Зарплата не указана"
            if salary:
                s_from = salary.get("from")
                s_to = salary.get("to")
                currency = salary.get("currency") or ""
                if s_from and s_to:
                    salary_text = f"{s_from:,} — {s_to:,} {currency}".replace(",", " ")
                elif s_from:
                    salary_text = f"от {s_from:,} {currency}".replace(",", " ")
                elif s_to:
                    salary_text = f"до {s_to:,} {currency}".replace(",", " ")

            employer = v.get("employer") or {}
            area_obj = v.get("area") or {}
            experience_obj = v.get("experience") or {}
            snippet = v.get("snippet") or {}

            items.append({
                "id": v.get("id", ""),
                "name": v.get("name", ""),
                "salary_text": salary_text,
                "employer_name": employer.get("name", ""),
                "employer_logo": (employer.get("logo_urls") or {}).get("90"),
                "area": area_obj.get("name", ""),
                "experience": experience_obj.get("name", ""),
                "published_at": v.get("published_at", ""),
                "url": v.get("alternate_url", ""),
                "requirement": snippet.get("requirement") or "",
                "responsibility": snippet.get("responsibility") or "",
            })

        return {
            "items": items,
            "found": data.get("found", 0),
            "pages": data.get("pages", 0),
            "page": data.get("page", 0),
        }

    except httpx.HTTPStatusError as e:
        return {"error": f"HH.ru API error: {e.response.status_code}", "items": [], "found": 0, "pages": 0, "page": 0}
    except Exception as e:
        return {"error": str(e), "items": [], "found": 0, "pages": 0, "page": 0}


@app.get("/api/healthz")
def health():
    return {"status": "ok"}
