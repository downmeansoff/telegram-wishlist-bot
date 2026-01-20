import { Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import { userAPI, wishesAPI } from '@/services/api'
import { useTelegram } from '@/hooks/useTelegram'

export default function HomePage() {
  const { user } = useTelegram()

  const { data: profile } = useQuery('profile', () =>
    userAPI.getProfile().then(res => res.data)
  )

  const { data: wishesData } = useQuery('recent-wishes', () =>
    wishesAPI.getWishes({ page: 1, page_size: 3 }).then(res => res.data)
  )

  const getPriorityColor = (priority: number) => {
    const colors = {
      1: 'bg-green-100 text-green-800',
      2: 'bg-yellow-100 text-yellow-800',
      3: 'bg-orange-100 text-orange-800',
      4: 'bg-red-100 text-red-800',
    }
    return colors[priority as keyof typeof colors] || colors[2]
  }

  return (
    <div className="min-h-screen bg-telegram-bg p-4">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-telegram-text mb-2">
          Привет, {user?.first_name}! 👋
        </h1>
        <p className="text-telegram-hint">
          Добро пожаловать в твой список желаний
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        <div className="bg-telegram-secondaryBg rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-telegram-text">
            {profile?.wishes_count || 0}
          </div>
          <div className="text-sm text-telegram-hint">Желаний</div>
        </div>
        <div className="bg-telegram-secondaryBg rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-telegram-text">
            {profile?.completed_wishes_count || 0}
          </div>
          <div className="text-sm text-telegram-hint">Выполнено</div>
        </div>
        <div className="bg-telegram-secondaryBg rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-telegram-text">
            {profile?.groups_count || 0}
          </div>
          <div className="text-sm text-telegram-hint">Групп</div>
        </div>
      </div>

      {/* Recent Wishes */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-telegram-text">
            Последние желания
          </h2>
          <Link
            to="/wishes"
            className="text-telegram-link text-sm font-medium"
          >
            Все →
          </Link>
        </div>

        {wishesData?.items?.length > 0 ? (
          <div className="space-y-3">
            {wishesData.items.map((wish: any) => (
              <Link
                key={wish.id}
                to={`/wishes/${wish.id}`}
                className="block bg-telegram-secondaryBg rounded-lg p-4 hover:opacity-80 transition fade-in"
              >
                <div className="flex items-start gap-3">
                  {wish.image_url && (
                    <img
                      src={wish.image_url}
                      alt={wish.title}
                      className="w-16 h-16 rounded-lg object-cover"
                    />
                  )}
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-telegram-text truncate">
                      {wish.title}
                    </h3>
                    {wish.description && (
                      <p className="text-sm text-telegram-hint truncate mt-1">
                        {wish.description}
                      </p>
                    )}
                    <div className="flex items-center gap-2 mt-2">
                      <span
                        className={`text-xs px-2 py-1 rounded ${getPriorityColor(
                          wish.priority
                        )}`}
                      >
                        Приоритет {wish.priority}
                      </span>
                      {wish.price && (
                        <span className="text-sm font-medium text-telegram-text">
                          {wish.price} {wish.currency}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="bg-telegram-secondaryBg rounded-lg p-8 text-center">
            <p className="text-telegram-hint mb-4">
              У тебя пока нет желаний
            </p>
            <Link
              to="/wishes/add"
              className="inline-block bg-telegram-button text-telegram-buttonText px-6 py-2 rounded-lg font-medium"
            >
              Добавить желание
            </Link>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 gap-3">
        <Link
          to="/wishes/add"
          className="bg-telegram-button text-telegram-buttonText rounded-lg p-4 text-center font-medium hover:opacity-80 transition"
        >
          ➕ Добавить желание
        </Link>
        <Link
          to="/groups"
          className="bg-telegram-secondaryBg text-telegram-text rounded-lg p-4 text-center font-medium hover:opacity-80 transition"
        >
          👥 Группы
        </Link>
      </div>
    </div>
  )
}
