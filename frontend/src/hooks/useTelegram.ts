import { useEffect, useState } from 'react'

declare global {
  interface Window {
    Telegram?: {
      WebApp: any
    }
  }
}

export const useTelegram = () => {
  const [webApp, setWebApp] = useState<any>(null)
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Wait for Telegram WebApp SDK to load
    const checkTelegram = () => {
      const tg = window.Telegram?.WebApp

      console.log('Checking Telegram WebApp:', tg)
      console.log('initDataUnsafe:', tg?.initDataUnsafe)

      if (tg) {
        setWebApp(tg)
        setUser(tg.initDataUnsafe?.user)
        setLoading(false)
      }
    }

    // Try immediately
    checkTelegram()

    // If not loaded, wait a bit and try again
    const timeout = setTimeout(() => {
      checkTelegram()
      setLoading(false) // Stop loading after timeout even if SDK not found
    }, 1000)

    return () => clearTimeout(timeout)
  }, [])

  return {
    webApp,
    user,
    loading,
    initData: webApp?.initData || '',
    colorScheme: webApp?.colorScheme || 'light',
  }
}
