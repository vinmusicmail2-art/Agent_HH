from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import httpx
import os
from typing import Optional

app = FastAPI(title="HH Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

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
        "search_field": "name",
        "query": "\"AI-креатор\" OR \"AI креатор\""
    },
    {
        "id": "ai_artist", "type": "job",
        "name": "AI-художник",
        "icon": "🎨",
        "search_field": "name",
        "query": "\"AI-художник\" OR \"AI художник\""
    },
    {
        "id": "ai_videomaker", "type": "job",
        "name": "AI-видеомейкер",
        "icon": "🎥",
        "search_field": "name",
        "query": "\"AI-видеомейкер\" OR \"AI видеомейкер\""
    },
    {
        "id": "ai_video_content", "type": "job",
        "name": "Специалист по AI-видеоконтенту",
        "icon": "📱",
        "search_field": "name",
        "query": "\"AI-видеоконтент\" OR \"AI видеоконтент\" OR \"создание AI-видео\" OR \"специалист по AI-видео\""
    },
    {
        "id": "ai_gen_video", "type": "job",
        "name": "Специалист по генерации видео (нейросети)",
        "icon": "⚡",
        "search_field": "name",
        "query": "\"генерация видео\" AND нейросети OR \"генерация AI-видео\" OR \"специалист по генерации видео\""
    },
    {
        "id": "ai_factory", "type": "job",
        "name": "AI Factory специалист",
        "icon": "🏭",
        "search_field": "name",
        "query": "\"AI Factory\" OR \"AI-Factory\""
    },
    {
        "id": "content_maker_ai", "type": "job",
        "name": "Контент-мейкер (AI video)",
        "icon": "✨",
        "search_field": "name",
        "query": "\"контент-мейкер\" AND (AI OR нейросети) OR \"AI video\" AND контент OR \"контент-мейкер AI\""
    },
    {
        "id": "editor_ai", "type": "job",
        "name": "Видеомонтажер с нейросетями",
        "icon": "🖥️",
        "search_field": "name",
        "query": "\"видеомонтажер\" AND нейросети OR \"монтажер\" AND нейросети OR \"монтажер\" AND AI"
    },
    {
        "id": "ai_artist_anim", "type": "job",
        "name": "AI artist (видео / анимация)",
        "icon": "🌀",
        "search_field": "name",
        "query": "\"AI artist\" OR \"AI-artist\""
    },
    {
        "id": "creator_ai", "type": "job",
        "name": "Креатор видеоконтента (нейросети)",
        "icon": "💡",
        "search_field": "name",
        "query": "\"креатор видеоконтента\" OR \"креатор\" AND нейросети OR \"креатор\" AND ИИ"
    },
    {
        "id": "ai_animation", "type": "job",
        "name": "Специалист по AI-анимации",
        "icon": "🎭",
        "search_field": "name",
        "query": "\"AI-анимация\" OR \"AI анимация\" OR \"специалист по анимации\" AND AI"
    },
    {
        "id": "ai_production", "type": "job",
        "name": "Видеопродакшн с ИИ",
        "icon": "🎞️",
        "search_field": "name",
        "query": "\"видеопродакшн\" AND (ИИ OR AI OR нейросети) OR \"продакшн\" AND AI"
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
        "search_field": "name",
        "query": "\"режиссер монтажа\" OR \"режиссёр монтажа\""
    },
    {
        "id": "edit_director_promo", "type": "job",
        "name": "Режиссер монтажа (промо)",
        "icon": "📺",
        "search_field": "name",
        "query": "\"режиссер монтажа\" AND (промо OR трейлер OR тизер) OR \"режиссёр монтажа\" AND (промо OR трейлер)"
    },
    {
        "id": "edit_director_news", "type": "job",
        "name": "Режиссер монтажа (новости)",
        "icon": "📰",
        "search_field": "name",
        "query": "\"режиссер монтажа\" AND (новости OR новостной) OR \"режиссёр монтажа\" AND новости"
    },
    {
        "id": "videoeditor", "type": "job",
        "name": "Видеомонтажер",
        "icon": "✂️",
        "search_field": "name",
        "query": "\"видеомонтажер\" OR \"видео-монтажер\""
    },
    {
        "id": "editor_tech", "type": "job",
        "name": "Монтажер",
        "icon": "🔧",
        "search_field": "name",
        "query": "монтажер AND (видео OR хроника OR \"Premiere Pro\" OR \"DaVinci\" OR \"Final Cut\")"
    },
    {
        "id": "videographer_editor", "type": "job",
        "name": "Видеограф-монтажер",
        "icon": "📷",
        "search_field": "name",
        "query": "\"видеограф-монтажер\" OR \"видеограф монтажер\""
    },
    {
        "id": "operator_editor", "type": "job",
        "name": "Оператор-монтажер",
        "icon": "🎦",
        "search_field": "name",
        "query": "\"оператор-монтажер\" OR \"оператор монтажер\""
    },
    {
        "id": "edit_director2", "type": "job",
        "name": "Режиссер видеомонтажа",
        "icon": "🎬",
        "search_field": "name",
        "query": "\"режиссер видеомонтажа\" OR \"режиссёр видеомонтажа\""
    },
    {
        "id": "lead_editor", "type": "job",
        "name": "Ведущий режиссер монтажа",
        "icon": "👑",
        "search_field": "name",
        "query": "\"ведущий режиссер монтажа\" OR \"ведущий режиссёр монтажа\" OR \"старший монтажер\" AND видео"
    },
    {
        "id": "asst_editor", "type": "job",
        "name": "Ассистент режиссера монтажа",
        "icon": "📋",
        "search_field": "name",
        "query": "\"ассистент режиссера монтажа\" OR \"ассистент монтажа\" OR \"помощник монтажера\""
    },
    {
        "id": "postprod_head", "type": "job",
        "name": "Руководитель постпродакшна",
        "icon": "🏆",
        "search_field": "name",
        "query": "\"руководитель постпродакшна\" OR \"руководитель пост-продакшн\" OR \"head of post-production\""
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
        "search_field": "name",
        "query": "\"оператор видеозаписи\" OR \"видеооператор\""
    },
    {
        "id": "videographer", "type": "job",
        "name": "Видеограф",
        "icon": "🤳",
        "search_field": "name",
        "query": "видеограф"
    },
    {
        "id": "correspondent", "type": "job",
        "name": "Корреспондент (видеомонтаж)",
        "icon": "🎤",
        "search_field": "name",
        "query": "корреспондент AND (видео OR монтаж OR съемка)"
    },
    {
        "id": "tv_journalist", "type": "job",
        "name": "Тележурналист",
        "icon": "📡",
        "search_field": "name",
        "query": "\"тележурналист\" OR \"телевизионный журналист\""
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
        "search_field": "name",
        "query": "\"цветокорректор\" OR \"колорист\" OR \"colorist\""
    },
    {
        "id": "postprod_spec", "type": "job",
        "name": "Специалист по постпродакшну",
        "icon": "⚙️",
        "search_field": "name",
        "query": "\"специалист по постпродакшну\" OR \"специалист пост-продакшн\" OR постпродакшн AND специалист"
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
        "search_field": "name",
        "query": "\"звукорежиссер\" OR \"звукорежиссёр\""
    },
    {
        "id": "sound_postprod", "type": "job",
        "name": "Звукорежиссер пост-продакшн",
        "icon": "🎛️",
        "search_field": "name",
        "query": "\"звукорежиссер\" AND (постпродакшн OR \"пост-продакшн\" OR озвучивание OR ADR)"
    },
    {
        "id": "sound_producer", "type": "job",
        "name": "Саунд-продюсер",
        "icon": "🎼",
        "search_field": "name",
        "query": "\"саунд-продюсер\" OR \"саунд продюсер\" OR \"sound producer\""
    },
    {
        "id": "mastering", "type": "job",
        "name": "Мастеринг-инженер",
        "icon": "🔊",
        "search_field": "name",
        "query": "\"мастеринг-инженер\" OR \"mastering engineer\" OR \"мастеринг инженер\""
    },
    {
        "id": "mixing", "type": "job",
        "name": "Специалист по сведению",
        "icon": "🎹",
        "search_field": "name",
        "query": "\"специалист по сведению\" OR \"сведение и мастеринг\" OR специалист AND (сведение OR мастеринг) AND аудио"
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
        "search_field": "name",
        "query": "\"контент-мейкер\" OR \"контент мейкер\""
    },
    {
        "id": "smm_content", "type": "job",
        "name": "SMM-менеджер / Контент-мейкер",
        "icon": "📣",
        "search_field": "name",
        "query": "SMM AND \"контент-мейкер\" OR \"SMM-менеджер\" AND контент OR \"SMM\" AND \"контент мейкер\""
    },
    {
        "id": "reelsmaker", "type": "job",
        "name": "Рилсмейкер",
        "icon": "📸",
        "search_field": "name",
        "query": "\"рилсмейкер\" OR \"рилс-мейкер\" OR \"reels maker\""
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
        "search_field": "name",
        "query": "\"вайбкодер\" OR \"вайб-кодер\" OR \"вайбкодинг\" OR \"vibe coder\" OR \"vibe coding\" OR \"vibe developer\" OR \"AI-native coder\" OR \"AI-first coder\" OR \"вайб-разработчик\" OR \"вайб-программист\""
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
        "search_field": "name",
        "query": "фотограф AND (видео OR продакшн OR анимация OR съемки)"
    },
    {
        "id": "drone_op", "type": "job",
        "name": "Оператор дрона",
        "icon": "🚁",
        "search_field": "name",
        "query": "\"оператор дрона\" OR \"дрон-оператор\" OR \"аэросъемка\" OR \"квадрокоптер\" AND оператор"
    },
    {
        "id": "targetolog", "type": "job",
        "name": "Таргетолог (видеокреативы)",
        "icon": "🎯",
        "search_field": "name",
        "query": "таргетолог AND (видео OR креатив)"
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
    period: Optional[int] = Query(None),
    education: Optional[str] = Query(None),
    schedule: Optional[str] = Query(None),
    employment: Optional[str] = Query(None),
    order_by: Optional[str] = Query(None),
    search_field: Optional[str] = Query(None),
    page: int = Query(0),
    per_page: int = Query(20),
):
    params = {
        "text": query,
        "page": page,
        "per_page": min(per_page, 100),
        "order_by": order_by if order_by else "relevance",
    }
    if search_field:
        params["search_field"] = search_field
    if area:
        params["area"] = area
    if salary_from:
        params["salary"] = salary_from
        params["only_with_salary"] = "true"
    if experience:
        params["experience"] = experience
    if period:
        params["period"] = period
    if education:
        params["education"] = education
    if schedule:
        params["schedule"] = schedule
    if employment:
        params["employment"] = employment

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


@app.get("/api/vacancy/{vacancy_id}")
async def get_vacancy(vacancy_id: str):
    headers = {
        "User-Agent": "HH-Agent/1.0 (job search application)",
        "HH-User-Agent": "HH-Agent/1.0 (job search application)",
    }
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                f"{HH_API_URL}/vacancies/{vacancy_id}",
                headers=headers,
            )
            response.raise_for_status()
            v = response.json()

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
        employment_obj = v.get("employment") or {}
        schedule_obj = v.get("schedule") or {}
        key_skills = [s.get("name", "") for s in (v.get("key_skills") or [])]

        return {
            "id": v.get("id", ""),
            "name": v.get("name", ""),
            "salary_text": salary_text,
            "employer_name": employer.get("name", ""),
            "employer_logo": (employer.get("logo_urls") or {}).get("90"),
            "employer_url": employer.get("alternate_url", ""),
            "area": area_obj.get("name", ""),
            "experience": experience_obj.get("name", ""),
            "employment": employment_obj.get("name", ""),
            "schedule": schedule_obj.get("name", ""),
            "published_at": v.get("published_at", ""),
            "url": v.get("alternate_url", ""),
            "description": v.get("description", ""),
            "key_skills": key_skills,
        }
    except httpx.HTTPStatusError as e:
        return {"error": f"HH.ru API error: {e.response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/healthz")
def health():
    return {"status": "ok"}


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
