import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from 'react-query'
import { groupsAPI } from '@/services/api'

export default function GroupDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const { data: group, isLoading } = useQuery(['group', id], () =>
    groupsAPI.getGroup(Number(id)).then(res => res.data)
  )

  const { data: wishes } = useQuery(['group-wishes', id], () =>
    groupsAPI.getGroupWishes(Number(id)).then(res => res.data)
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

      <h1 className="text-2xl font-bold text-telegram-text mb-2">
        {group?.name}
      </h1>

      {group?.description && (
        <p className="text-telegram-hint mb-4">{group.description}</p>
      )}

      <div className="bg-telegram-secondaryBg rounded-lg p-4 mb-6">
        <p className="text-sm text-telegram-hint mb-2">Код приглашения:</p>
        <code className="text-lg font-mono text-telegram-text">
          {group?.invite_code}
        </code>
      </div>

      <h2 className="text-xl font-semibold text-telegram-text mb-4">
        Желания участников
      </h2>

      {wishes?.length > 0 ? (
        <div className="space-y-3">
          {wishes.map((wish: any) => (
            <div
              key={wish.id}
              className="bg-telegram-secondaryBg rounded-lg p-4"
            >
              <h3 className="font-medium text-telegram-text">{wish.title}</h3>
              {wish.price && (
                <p className="text-sm text-telegram-hint mt-1">
                  {wish.price} {wish.currency}
                </p>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-center text-telegram-hint py-8">
          Пока нет желаний
        </p>
      )}
    </div>
  )
}
