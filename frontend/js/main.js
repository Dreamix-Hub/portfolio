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
      if (visibleCount === 0) {
        projectsEmpty.classList.remove('hidden')
      } else {
        projectsEmpty.classList.add('hidden')
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
      blogEmpty.classList.toggle('hidden', visible > 0)

      // Update count
      if (blogCount) {
        blogCount.textContent = `${visible} post${visible !== 1 ? 's' : ''}`
      }
    })
  })
}