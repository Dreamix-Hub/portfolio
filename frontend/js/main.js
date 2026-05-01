/* ============================================================
   HAMBURGER MENU
   ============================================================ */

const hamburger  = document.getElementById('hamburger')
const navDrawer  = document.getElementById('navDrawer')
const navOverlay = document.getElementById('navOverlay')

function openMenu() {
  hamburger.classList.add('open')
  navDrawer.classList.add('open')
  navOverlay.classList.add('open')
  hamburger.setAttribute('aria-expanded', 'true')
  document.body.style.overflow = 'hidden'
}

function closeMenu() {
  hamburger.classList.remove('open')
  navDrawer.classList.remove('open')
  navOverlay.classList.remove('open')
  hamburger.setAttribute('aria-expanded', 'false')
  document.body.style.overflow = ''
}

if (hamburger) {
  hamburger.addEventListener('click', () => {
    hamburger.classList.contains('open') ? closeMenu() : openMenu()
  })
}

if (navOverlay) {
  navOverlay.addEventListener('click', closeMenu)
}

// Close menu on nav link click (mobile)
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', closeMenu)
})

// Close menu on nav action button click (resume and admin)
document.querySelectorAll('.nav-actions .btn').forEach(btn => {
  btn.addEventListener('click', closeMenu)
})

// Close menu when resizing to desktop
window.addEventListener('resize', () => {
  if (window.innerWidth >= 768) closeMenu()
})

// Close on Escape key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeMenu()
})


/* ============================================================
   TYPING ANIMATION
   ============================================================ */

const roles = [
  'Backend Developer',
  'AI / ML Engineer',
  'FastAPI Specialist',
  'CS Final Year Student',
]

let roleIndex  = 0
let charIndex  = 0
let isDeleting = false
const typingEl = document.getElementById('typingText')

function type() {
  if (!typingEl) return

  const current = roles[roleIndex]

  if (isDeleting) {
    typingEl.textContent = current.substring(0, charIndex - 1)
    charIndex--
  } else {
    typingEl.textContent = current.substring(0, charIndex + 1)
    charIndex++
  }

  let speed = isDeleting ? 60 : 110

  if (!isDeleting && charIndex === current.length) {
    speed = 1800
    isDeleting = true
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false
    roleIndex = (roleIndex + 1) % roles.length
    speed = 400
  }

  setTimeout(type, speed)
}

document.addEventListener('DOMContentLoaded', () => {
  if (typingEl) setTimeout(type, 600)
})


/* ============================================================
   NAVBAR ACTIVE LINK — auto-detect current page
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  const links   = document.querySelectorAll('.nav-link')
  const current = window.location.pathname.split('/').pop() || 'index.html'

  links.forEach(link => {
    const href = link.getAttribute('href').split('/').pop()
    link.classList.remove('active')
    if (href === current) link.classList.add('active')
  })
})

/* ============================================================
   PROJECTS — FILTER
   ============================================================ */

const filterBtns    = document.querySelectorAll('.filter-btn')
const projectsGrid  = document.getElementById('projectsGrid')
const projectsEmpty = document.getElementById('projectsEmpty')
const projectsCount = document.getElementById('projectsCount')

if (filterBtns.length) {

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {

      // Update active button
      filterBtns.forEach(b => b.classList.remove('active'))
      btn.classList.add('active')

      const filter = btn.dataset.filter

      // Featured card
      const featured = document.querySelector('.project-card--featured')
      if (featured) {
        const featuredTags = featured.dataset.tags.split(' ')
        if (filter === 'all' || featuredTags.includes(filter)) {
          featured.classList.remove('hidden')
        } else {
          featured.classList.add('hidden')
        }
      }

      // Regular cards
      const cards = document.querySelectorAll('.project-card--regular')
      let visibleCount = featured && !featured.classList.contains('hidden') ? 1 : 0

      cards.forEach(card => {
        const tags = card.dataset.tags.split(' ')
        if (filter === 'all' || tags.includes(filter)) {
          card.classList.remove('hidden')
          visibleCount++
        } else {
          card.classList.add('hidden')
        }
      })

      // Show / hide empty state
      if (projectsEmpty) {
        if (visibleCount === 0) {
          projectsEmpty.classList.remove('hidden')
        } else {
          projectsEmpty.classList.add('hidden')
        }
      }

      // Update count
      if (projectsCount) {
        projectsCount.textContent = `${visibleCount} project${visibleCount !== 1 ? 's' : ''}`
      }
    })
  })
}


/* ============================================================
   BLOG — TAG FILTER
   ============================================================ */

const blogFilterBtns = document.querySelectorAll('#blogFilterBar .filter-btn')
const blogEmpty      = document.getElementById('blogEmpty')
const blogCount      = document.getElementById('blogCount')

if (blogFilterBtns.length) {

  blogFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {

      // Update active button
      blogFilterBtns.forEach(b => b.classList.remove('active'))
      btn.classList.add('active')

      const filter = btn.dataset.filter

      // Featured card
      const featured = document.querySelector('.blog-card--featured')
      if (featured) {
        const featuredTags = featured.dataset.tags.split(' ')
        featured.classList.toggle(
          'hidden',
          filter !== 'all' && !featuredTags.includes(filter)
        )
      }

      // Regular cards
      const cards = document.querySelectorAll('.blog-card--regular')
      let visible = featured && !featured.classList.contains('hidden') ? 1 : 0

      cards.forEach(card => {
        const tags = card.dataset.tags.split(' ')
        const show = filter === 'all' || tags.includes(filter)
        card.classList.toggle('hidden', !show)
        if (show) visible++
      })

      // Empty state
      if (blogEmpty) {
        blogEmpty.classList.toggle('hidden', visible > 0)
      }

      // Update count
      if (blogCount) {
        blogCount.textContent = `${visible} post${visible !== 1 ? 's' : ''}`
      }
    })
  })
}

/* ============================================================
   BLOG POST PAGE
   ============================================================ */

/* ------------------------------------------------------------------
   LOCAL POST DATA
   This is placeholder data so the page works before the backend
   is connected. When FastAPI is ready, replace loadPost() with
/* ============================================================
   BLOG POST PAGE — LOCAL DATA
   ============================================================ */


const POSTS = {
  'virtual-tryon-api': {
    title:     'Building a Virtual Try-On API with IDM-VTON and FastAPI',
    tags:      ['FASTAPI', 'AI / ML'],
    date:      'Apr 12, 2025',
    readTime:  '8 min read',
    views:     142,
    cover:     null,
    content: `
## Introduction

Virtual try-on is one of the most exciting applications of generative AI in
e-commerce. Instead of relying on static product images, customers can see how
a garment looks on their own body before purchasing. In this post I'll walk
through how I integrated **IDM-VTON** — a diffusion-based try-on model — into
a production-ready FastAPI backend.

## What is IDM-VTON?

IDM-VTON (Improving Diffusion Models for Virtual Try-ON) is a state-of-the-art
model that takes two inputs:

- A **person image** (the user's photo)
- A **garment image** (the product to try on)

And produces a realistic composite image showing the person wearing the garment.

## The preprocessing challenge

Before IDM-VTON can run, the person image needs to be **parsed** — we need to
know which pixels belong to the torso, arms, legs, background, etc. This is
where **SCHP** (Self-Correction for Human Parsing) comes in.

\`\`\`python
from schp import HumanParser

parser = HumanParser(model_path="checkpoints/schp.pth")

def preprocess(image_path: str) -> dict:
    parsed = parser.parse(image_path)
    return {
        "parse_map": parsed["label_map"],
        "parse_agnostic": parsed["agnostic"],
    }
\`\`\`

## Integrating with FastAPI

The key challenge is that model inference is CPU/GPU-bound — it blocks the
event loop if you run it directly in an async route. The fix is to offload it
to a **thread pool executor**.

\`\`\`python
import asyncio
from fastapi import FastAPI, UploadFile
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=2)

@app.post("/tryon")
async def tryon(person: UploadFile, garment: UploadFile):
    person_bytes  = await person.read()
    garment_bytes = await garment.read()

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        run_inference,
        person_bytes,
        garment_bytes,
    )
    return {"image": result}
\`\`\`

## Deployment gotchas

> Running PyTorch models in Docker requires careful CUDA version pinning.
> Mismatches between the base image, torch, and CUDA driver version will
> silently fall back to CPU — or crash entirely.

A few things I learned the hard way:

- Always pin \`torch\` and \`torchvision\` to the **exact** same CUDA build
- Use multi-stage Docker builds to keep the final image lean
- Set \`PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512\` to avoid OOM errors

## Conclusion

Integrating a diffusion model into a FastAPI backend is very doable once you
understand the async / thread pool pattern and sort out your Docker CUDA
setup. In the next post I'll cover how I handle **result caching** with
Supabase Storage so users don't wait for inference on repeated requests.
    `
  },

  'async-sqlalchemy-fastapi': {
    title:     'Async SQLAlchemy with FastAPI — the right way',
    tags:      ['DATABASES'],
    date:      'Mar 28, 2025',
    readTime:  '5 min read',
    views:     98,
    cover:     null,
    content: `
## The problem with sync SQLAlchemy

If you use SQLAlchemy's standard synchronous sessions inside an async FastAPI
route, you block the event loop on every database call. Under load, this
destroys your concurrency.

## Setting up async sessions

\`\`\`python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
\`\`\`

## The dependency pattern

\`\`\`python
from fastapi import Depends

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
\`\`\`

> Always use \`expire_on_commit=False\` with async sessions. Without it,
> accessing attributes after a commit raises a lazy-loading error because
> async SQLAlchemy can't implicitly await the attribute load.

## The missing await bug

One of the most common bugs I ran into was forgetting to \`await\` the
session call inside an exception handler — which causes a \`TypeError\`
because the coroutine is never awaited. Always double-check your
exception handlers.
    `
  },

  'dockerizing-fastapi-ml': {
    title:     'Dockerizing a FastAPI + ML model app from scratch',
    tags:      ['DEVOPS'],
    date:      'Mar 10, 2025',
    readTime:  '6 min read',
    views:     76,
    cover:     null,
    content: `
## Why ML apps are different to dockerize

A standard FastAPI app Dockerfile is straightforward. Add PyTorch and a
pre-trained model and suddenly you're dealing with:

- 5GB+ image sizes
- CUDA driver compatibility issues
- Slow cold starts from model loading

## Multi-stage builds

\`\`\`dockerfile
# Stage 1 — builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2 — runtime
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
\`\`\`

## Pinning CUDA versions

Always match your torch install to the exact CUDA version on your host:

\`\`\`bash
pip install torch==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118
\`\`\`

## Keeping images lean

- Use \`.dockerignore\` to exclude \`__pycache__\`, \`.git\`, and model checkpoints
- Download model weights at runtime from Supabase Storage instead of baking them into the image
- Use \`--no-cache-dir\` on every pip install
    `
  },

  'jwt-fastapi-swagger-bug': {
    title:     'JWT auth in FastAPI — fixing the Swagger UI bug',
    tags:      ['FASTAPI'],
    date:      'Feb 19, 2025',
    readTime:  '4 min read',
    views:     211,
    cover:     null,
    content: `
## The bug

You set up JWT auth in FastAPI, open Swagger UI at \`/docs\`, click
**Authorize**, enter your credentials — and nothing works. Requests still come
back as 401.

## The root cause

Almost always the issue is one of two things:

**1. oauth2_scheme not wrapped in Depends()**

\`\`\`python
# ❌ Wrong — oauth2_scheme called directly
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/me")
async def get_me(token: str = oauth2_scheme):  # missing Depends()
    ...

# ✅ Correct
@app.get("/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    ...
\`\`\`

**2. tokenUrl mismatch**

\`\`\`python
# The tokenUrl must exactly match your login route path
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

@app.post("/api/v1/auth/token")  # must match exactly
async def login(form: OAuth2PasswordRequestForm = Depends()):
    ...
\`\`\`

## Verifying the fix

After fixing, reload Swagger UI, click Authorize, enter your username and
password. Swagger will POST to your token endpoint, receive the JWT, and
attach it automatically as a \`Bearer\` header on every subsequent request.

> If it still doesn't work after fixing both issues, check that your token
> endpoint returns \`{"access_token": "...", "token_type": "bearer"}\` —
> Swagger requires the \`token_type\` field to be present.
    `
  },

  'fyp-backend-lessons': {
    title:     'What I learned building my FYP as a backend solo dev',
    tags:      ['CAREER'],
    date:      'Jan 30, 2025',
    readTime:  '7 min read',
    views:     54,
    cover:     null,
    content: `
## Context

For my Final Year Project I own the entire backend — API design, database
schema, AI model integration, cloud deployment, and coordination with a
frontend teammate. Here's what I learned.

## Design the API contract first

Before writing a single line of backend code, write out every endpoint your
frontend will need. Agree on the request/response shapes. This saves enormous
back-and-forth later.

\`\`\`
POST /api/tryon
  body: { person_image, garment_image }
  response: { result_url, processing_time_ms }

GET /api/blogs
  response: [{ id, title, slug, tags, date, views }]
\`\`\`

## Don't underestimate model loading time

PyTorch models can take **15–30 seconds** to load from disk. Load them once at
startup, not on every request:

\`\`\`python
@app.on_event("startup")
async def startup():
    app.state.model = load_model("checkpoints/idm_vton.pth")
\`\`\`

## Keep secrets out of code

Use a \`.env\` file and \`python-dotenv\` from day one. I made the mistake of
hardcoding a Supabase URL in an early commit — even in a private repo, this
is a bad habit to form.

## Async is not optional for ML backends

If you block the event loop during inference, your entire API becomes
unresponsive for every other request. Use \`run_in_executor\` for all
CPU-bound work from day one.

## Communicate schema changes immediately

When you need to change a database schema, tell your frontend teammate the
same day. A broken response shape that slips through wastes hours of debugging
on both sides.
    `
  },

  'schp-human-parsing': {
    title:     'Understanding SCHP for human parsing in try-on systems',
    tags:      ['AI / ML'],
    date:      'Jan 12, 2025',
    readTime:  '9 min read',
    views:     88,
    cover:     null,
    content: `
## What is human parsing?

Human parsing is a computer vision task that assigns a **semantic label** to
every pixel in an image of a person — torso, left arm, right leg, hair,
background, and so on. It's a prerequisite for virtual try-on because the
model needs to know exactly where the garment should be placed.

## What is SCHP?

**Self-Correction for Human Parsing** is a model that improves accuracy by
running an iterative self-correction mechanism — it parses the image, then
uses the parse result to refine itself in a second pass.

## Why SCHP specifically?

Most try-on systems I looked at used LIP or ATR datasets for parsing, but SCHP
consistently produced cleaner boundaries on the torso region — which is exactly
what matters for upper-body garment try-on.

## How it fits into the pipeline

\`\`\`
Person Image
     │
     ▼
┌──────────┐
│   SCHP   │  → parse map (20 classes)
└──────────┘  → agnostic image (person without original top)
     │
     ▼
┌───────────┐
│ IDM-VTON  │  ← garment image
└───────────┘
     │
     ▼
 Result Image
\`\`\`

## Common issues

- **Blurry boundaries**: usually caused by downscaling the input below 512px
- **Wrong labels on complex poses**: SCHP struggles with unusual body angles;
  adding a pose estimator as a second signal helps
- **Slow inference**: SCHP on CPU is usable for development but GPU is required
  in production — target under 200ms per image
    `
}
}
/* ------------------------------------------------------------------
   RENDER MARKDOWN
   A super simple markdown parser for blog post content.
   When you connect the FastAPI backend, you can replace this with
   a proper library like marked.js if your backend sends raw markdown.
-(hyphens)
*/

function renderMarkdown(md) {
  let html = md
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm,  '<h2>$1</h2>')
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]+?<\/li>)(?!\s*<li>)/g, '<ul>$1</ul>')
    .replace(/^---$/gm, '<hr>')
    .split('\n\n')
    .map(block => {
      block = block.trim()
      if (!block) return ''
      if (/^<(h[123]|pre|blockquote|ul|hr)/.test(block)) return block
      return `<p>${block.replace(/\n/g, '<br>')}</p>`
    })
    .join('\n')
  return html
}

/* ------------------------------------------------------------------
   LOAD & RENDER POST
*/

function initPostPage() {
  const postLoading  = document.getElementById('postLoading')
  const postNotFound = document.getElementById('postNotFound')
  const postArticle  = document.getElementById('postArticle')

  if (!postLoading) return

  const params = new URLSearchParams(window.location.search)
  const slug   = params.get('slug')

  setTimeout(() => {
    const post = POSTS[slug]
    postLoading.style.display = 'none'

    if (!post) {
      postNotFound.classList.remove('hidden')
      return
    }

    document.title = `${post.title} — Muhammad Abdullah`

    const badgesEl = document.getElementById('postBadges')
    badgesEl.innerHTML = post.tags
      .map(t => `<span class="project-badge project-badge--tag">${t}</span>`)
      .join('')

    document.getElementById('postTitle').textContent = post.title

    const metaEl = document.getElementById('postMeta')
    metaEl.innerHTML = `
      <span class="blog-meta-item">${post.date}</span>
      <span class="blog-meta-dot">·</span>
      <span class="blog-meta-item">${post.readTime}</span>
      <span class="blog-meta-dot">·</span>
      <span class="blog-meta-item blog-meta-views">${post.views} views</span>
    `

    if (post.cover) {
      const coverEl    = document.getElementById('postCover')
      const coverImg   = document.getElementById('postCoverImg')
      coverImg.src     = post.cover
      coverImg.alt     = post.title
      coverEl.classList.remove('hidden')
    }

    document.getElementById('postBody').innerHTML = renderMarkdown(post.content)
    postArticle.classList.remove('hidden')
  }, 500)
}

document.addEventListener('DOMContentLoaded', initPostPage)

/* ============================================================
   CONTACT FORM — VALIDATION & SUBMIT
   ============================================================ */

const contactForm    = document.getElementById('contactForm')
const contactSuccess = document.getElementById('contactSuccess')
const contactReset   = document.getElementById('contactSuccessReset')

/* ── Helpers ── */

function getVal(id) {
  const el = document.getElementById(id)
  return el ? el.value.trim() : ''
}

function setError(fieldId, errorId, msg) {
  const input = document.getElementById(fieldId)
  const error = document.getElementById(errorId)
  if (input) input.classList.toggle('error', !!msg)
  if (error) error.textContent = msg || ''
}

function clearErrors() {
  ;[
    ['contactName',    'nameError'],
    ['contactEmail',   'emailError'],
    ['contactSubject', 'subjectError'],
    ['contactMessage', 'messageError'],
  ].forEach(([field, err]) => setError(field, err, ''))
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

function validate() {
  clearErrors()
  let valid = true

  if (!getVal('contactName')) {
    setError('contactName', 'nameError', 'name is required')
    valid = false
  }

  const email = getVal('contactEmail')
  if (!email) {
    setError('contactEmail', 'emailError', 'email is required')
    valid = false
  } else if (!isValidEmail(email)) {
    setError('contactEmail', 'emailError', 'enter a valid email address')
    valid = false
  }

  if (!getVal('contactSubject')) {
    setError('contactSubject', 'subjectError', 'subject is required')
    valid = false
  }

  if (!getVal('contactMessage')) {
    setError('contactMessage', 'messageError', 'message is required')
    valid = false
  } else if (getVal('contactMessage').length < 10) {
    setError('contactMessage', 'messageError', 'message is too short')
    valid = false
  }

  return valid
}

/* ── Clear error on input ── */
;['contactName', 'contactEmail', 'contactSubject', 'contactMessage'].forEach(id => {
  const el = document.getElementById(id)
  if (!el) return
  el.addEventListener('input', () => {
    el.classList.remove('error')
    const errorMap = {
      contactName:    'nameError',
      contactEmail:   'emailError',
      contactSubject: 'subjectError',
      contactMessage: 'messageError',
    }
    const errEl = document.getElementById(errorMap[id])
    if (errEl) errEl.textContent = ''
  })
})

/* ── Submit ── */
if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault()

    if (!validate()) return

    const submitBtn = document.getElementById('contactSubmit')
    submitBtn.disabled = true
    submitBtn.textContent = 'sending...'

    const payload = {
      name:    getVal('contactName'),
      email:   getVal('contactEmail'),
      subject: getVal('contactSubject'),
      message: getVal('contactMessage'),
    }

    try {
      /*
       * BACKEND CONNECTION POINT
       * When your FastAPI /api/contact endpoint is ready,
       * uncomment the fetch below and remove the setTimeout mock.
       *
       * const res = await fetch('/api/contact', {
       *   method:  'POST',
       *   headers: { 'Content-Type': 'application/json' },
       *   body:    JSON.stringify(payload),
       * })
       * if (!res.ok) throw new Error('server error')
       */

      // Mock success — remove this when backend is connected
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Show success state
      contactForm.classList.add('hidden')
      contactSuccess.classList.remove('hidden')

    } catch (err) {
      // Show a general error on the message field
      setError('contactMessage', 'messageError', 'something went wrong. please try again.')
      submitBtn.disabled = false
      submitBtn.textContent = 'send message →'
    }
  })
}

/* ── Reset form ── */
if (contactReset) {
  contactReset.addEventListener('click', () => {
    contactSuccess.classList.add('hidden')
    contactForm.classList.remove('hidden')
    contactForm.reset()
    clearErrors()
    const submitBtn = document.getElementById('contactSubmit')
    if (submitBtn) {
      submitBtn.disabled = false
      submitBtn.textContent = 'send message →'
    }
  })
}