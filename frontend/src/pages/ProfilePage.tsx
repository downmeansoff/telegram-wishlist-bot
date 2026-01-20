import { useNavigate } from 'react-router-dom'
import { useQuery } from 'react-query'
import { userAPI } from '@/services/api'

export default function ProfilePage() {
  const navigate = useNavigate()

  const { data: profile, isLoading } = useQuery('profile', () =>
    userAPI.getProfile().then(res => res.data)
  )

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-telegram-button"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-telegram-bg p-4">
      <button onClick={() => navigate(-1)} className="text-telegram-link mb-4">
        ← Назад
      </button>

      <h1 className="text-2xl font-bold text-telegram-text mb-6">
        ⚙️ Профиль
      </h1>

      <div className="bg-telegram-secondaryBg rounded-lg p-4 mb-6">
        <h2 className="font-semibold text-telegram-text mb-4">
          Информация
        </h2>

        <div className="space-y-3">
          <div>
            <p className="text-sm text-telegram-hint">Имя</p>
            <p className="text-telegram-text">{profile?.first_name}</p>
          </div>

          {profile?.username && (
            <div>
              <p className="text-sm text-telegram-hint">Username</p>
              <p className="text-telegram-text">@{profile.username}</p>
            </div>
          )}

          <div>
            <p className="text-sm text-telegram-hint">Telegram ID</p>
            <p className="text-telegram-text font-mono">{profile?.telegram_id}</p>
          </div>
        </div>
      </div>

      <div className="bg-telegram-secondaryBg rounded-lg p-4">
        <h2 className="font-semibold text-telegram-text mb-4">
          Статистика
        </h2>

        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-telegram-text">
              {profile?.wishes_count || 0}
            </div>
            <div className="text-xs text-telegram-hint">Желаний</div>
          </div>

          <div className="text-center">
            <div className="text-2xl font-bold text-telegram-text">
              {profile?.completed_wishes_count || 0}
            </div>
            <div className="text-xs text-telegram-hint">Выполнено</div>
          </div>

          <div className="text-center">
            <div className="text-2xl font-bold text-telegram-text">
              {profile?.groups_count || 0}
            </div>
            <div className="text-xs text-telegram-hint">Групп</div>
          </div>
        </div>
      </div>
    </div>
  )
}
