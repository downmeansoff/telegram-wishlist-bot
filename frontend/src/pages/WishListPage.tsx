import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import { wishesAPI } from '@/services/api'
import { WishStatus } from '@/types'

export default function WishListPage() {
  const [status] = useState<WishStatus>(WishStatus.ACTIVE)
  const [search, setSearch] = useState('')

  const { data: wishesData, isLoading } = useQuery(
    ['wishes', status, search],
    () => wishesAPI.getWishes({ status, search }).then(res => res.data)
  )

  const getPriorityEmoji = (priority: number) => {
    const emojis = { 1: '🟢', 2: '🟡', 3: '🔴', 4: '⚡' }
    return emojis[priority as keyof typeof emojis] || '⚪'
  }

  return (
    <div className="min-h-screen bg-telegram-bg">
      {/* Header */}
      <div className="sticky top-0 bg-telegram-bg z-10 border-b border-gray-200 dark:border-gray-800">
        <div className="p-4">
          <h1 className="text-2xl font-bold text-telegram-text mb-4">
            🎁 Мои желания
          </h1>

          {/* Search */}
          <input
            type="text"
            placeholder="Поиск..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full px-4 py-2 rounded-lg bg-telegram-secondaryBg text-telegram-text placeholder-telegram-hint border-none focus:outline-none focus:ring-2 focus:ring-telegram-button"
          />
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-telegram-button"></div>
          </div>
        ) : wishesData?.items?.length > 0 ? (
          <div className="space-y-3 mb-20">
            {wishesData.items.map((wish: any) => (
              <Link
                key={wish.id}
                to={`/wishes/${wish.id}`}
                className="block bg-telegram-secondaryBg rounded-lg overflow-hidden hover:opacity-80 transition fade-in"
              >
                {wish.image_url && (
                  <img
                    src={wish.image_url}
                    alt={wish.title}
                    className="w-full h-48 object-cover"
                  />
                )}
                <div className="p-4">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <h3 className="font-semibold text-telegram-text flex-1">
                      {getPriorityEmoji(wish.priority)} {wish.title}
                    </h3>
                    {wish.price && (
                      <span className="font-bold text-telegram-text whitespace-nowrap">
                        {wish.price} {wish.currency}
                      </span>
                    )}
                  </div>
                  {wish.description && (
                    <p className="text-sm text-telegram-hint line-clamp-2">
                      {wish.description}
                    </p>
                  )}
                  {wish.link && (
                    <p className="text-xs text-telegram-link mt-2 truncate">
                      🔗 {wish.link}
                    </p>
                  )}
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-telegram-hint mb-4">
              {search ? 'Ничего не найдено' : 'Список пуст'}
            </p>
            {!search && (
              <Link
                to="/wishes/add"
                className="inline-block bg-telegram-button text-telegram-buttonText px-6 py-2 rounded-lg font-medium"
              >
                Добавить первое желание
              </Link>
            )}
          </div>
        )}
      </div>

      {/* FAB */}
      <Link
        to="/wishes/add"
        className="fixed bottom-6 right-6 w-14 h-14 bg-telegram-button text-telegram-buttonText rounded-full shadow-lg flex items-center justify-center text-2xl hover:scale-110 transition"
      >
        +
      </Link>
    </div>
  )
}
