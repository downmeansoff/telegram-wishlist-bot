import { Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import { groupsAPI } from '@/services/api'

export default function GroupsPage() {
  const { data: groups, isLoading } = useQuery('groups', () =>
    groupsAPI.getGroups().then(res => res.data)
  )

  return (
    <div className="min-h-screen bg-telegram-bg p-4">
      <h1 className="text-2xl font-bold text-telegram-text mb-6">
        👥 Мои группы
      </h1>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-telegram-button"></div>
        </div>
      ) : groups?.length > 0 ? (
        <div className="space-y-3">
          {groups.map((group: any) => (
            <Link
              key={group.id}
              to={`/groups/${group.id}`}
              className="block bg-telegram-secondaryBg rounded-lg p-4 hover:opacity-80 transition"
            >
              <h3 className="font-semibold text-telegram-text mb-1">
                {group.name}
              </h3>
              {group.description && (
                <p className="text-sm text-telegram-hint mb-2">
                  {group.description}
                </p>
              )}
              <p className="text-xs text-telegram-hint">
                👥 {group.member_count} участников
              </p>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-telegram-hint mb-4">У вас пока нет групп</p>
          <p className="text-sm text-telegram-hint">
            Создайте группу или присоединитесь по коду приглашения
          </p>
        </div>
      )}
    </div>
  )
}
