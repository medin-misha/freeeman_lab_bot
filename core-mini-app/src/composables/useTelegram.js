import {
  init,
  miniAppReady,
  mountMiniAppSync,
  setMiniAppHeaderColor,
  setMiniAppBackgroundColor,
  closeMiniApp,
  mountViewport,
  expandViewport,
  hapticFeedbackImpactOccurred,
  isHapticFeedbackSupported,
  restoreInitData,
  initDataUser
} from '@telegram-apps/sdk'

export function useTelegram() {
  async function initApp() {
    try {
      init()
      restoreInitData()
      mountMiniAppSync()
      miniAppReady()
      setMiniAppHeaderColor('#0A0A0A')
      setMiniAppBackgroundColor('#0A0A0A')
      await mountViewport()
      expandViewport()
    } catch (e) {
      console.warn('Telegram SDK init failed:', e)
    }
  }

  function haptic() {
    if (isHapticFeedbackSupported()) {
      hapticFeedbackImpactOccurred('light')
    }
  }

  function close() {
    closeMiniApp()
  }

  function getUser() {
    return initDataUser() ?? null
  }

  return { initApp, haptic, close, getUser }
}
