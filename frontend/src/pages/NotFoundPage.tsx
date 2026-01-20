import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-telegram-bg px-4">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-telegram-text mb-4">404</h1>
        <p className="text-xl text-telegram-hint mb-8">Страница не найдена</p>
        <Link
          to="/"
          className="inline-block bg-telegram-button text-telegram-buttonText px-6 py-3 rounded-lg font-medium hover:opacity-80 transition"
        >
          На главную
        </Link>
      </div>
    </div>
  )
}
