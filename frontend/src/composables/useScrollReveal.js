import { onMounted, onUnmounted, nextTick } from 'vue'

// Reveals any element with the `.reveal` class as it scrolls into view.
// Replaces the IntersectionObserver boilerplate that was duplicated in every view.
export function useScrollReveal() {
  let observer = null

  const observe = () => {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    )
    document.querySelectorAll('.reveal:not(.visible)').forEach((el) => observer.observe(el))
  }

  onMounted(() => nextTick(observe))
  onUnmounted(() => observer && observer.disconnect())

  // Lets callers re-scan after async content (e.g. a fetched list) renders.
  return { refresh: () => nextTick(observe) }
}
