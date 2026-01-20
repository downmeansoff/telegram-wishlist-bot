import { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useTelegram } from './hooks/useTelegram'

// Pages
import HomePage from './pages/HomePage'
import WishListPage from './pages/WishListPage'
import WishDetailPage from './pages/WishDetailPage'
import AddWishPage from './pages/AddWishPage'
import GroupsPage from './pages/GroupsPage'
import GroupDetailPage from './pages/GroupDetailPage'
import ProfilePage from './pages/ProfilePage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  const { webApp, user, loading } = useTelegram()

  useEffect(() => {
    console.log('WebApp:', webApp)
    console.log('User:', user)
    console.log('Loading:', loading)

    // Expand app to full height
    webApp?.expand()

    // Enable closing confirmation
    webApp?.enableClosingConfirmation()

    // Set header color
    webApp?.setHeaderColor('#3B82F6')

    // Ready
    webApp?.ready()
  }, [webApp, loading])

  // Show loading only while checking for Telegram SDK
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="text-center p-8 bg-white rounded-lg shadow-lg max-w-md mx-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-800 font-medium mb-2">Загрузка Telegram Web App...</p>
          <p className="text-xs text-gray-500">Пожалуйста, подождите</p>
        </div>
      </div>
    )
  }

  // If SDK didn't load but we're not loading anymore, show error
  if (!webApp) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-red-50">
        <div className="text-center p-8 bg-white rounded-lg shadow-lg max-w-md mx-4">
          <div className="text-red-500 text-5xl mb-4">⚠️</div>
          <p className="text-gray-800 font-medium mb-2">Telegram Web App SDK не загрузился</p>
          <p className="text-xs text-gray-500 mb-4">Это приложение должно открываться внутри Telegram</p>
          <p className="text-xs text-gray-400">Debug: window.Telegram = {typeof window.Telegram}</p>
        </div>
      </div>
    )
  }

  return (
    <Router>
      <div className="min-h-screen bg-telegram-bg">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/wishes" element={<WishListPage />} />
          <Route path="/wishes/:id" element={<WishDetailPage />} />
          <Route path="/wishes/add" element={<AddWishPage />} />
          <Route path="/groups" element={<GroupsPage />} />
          <Route path="/groups/:id" element={<GroupDetailPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>

        <Toaster
          position="top-center"
          toastOptions={{
            duration: 3000,
            style: {
              background: 'var(--tg-theme-secondary-bg-color)',
              color: 'var(--tg-theme-text-color)',
            },
          }}
        />
      </div>
    </Router>
  )
}

export default App
