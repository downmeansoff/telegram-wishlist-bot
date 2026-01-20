import { useNavigate, useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import toast from 'react-hot-toast'
import { wishesAPI } from '@/services/api'

export default function WishDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: wish, isLoading } = useQuery(['wish', id], () =>
    wishesAPI.getWish(Number(id)).then(res => res.data)
  )

  const completeMutation = useMutation(
    () => wishesAPI.completeWish(Number(id)),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['wish', id])
        queryClient.invalidateQueries('wishes')
        toast.success('Поздравляем! 🎉')
      },
    }
  )

  const deleteMutation = useMutation(
    () => wishesAPI.deleteWish(Number(id)),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('wishes')
        toast.success('Желание удалено')
        navigate('/wishes')
      },
    }
  )

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-telegram-button"></div>
      </div>
    )
  }

  if (!wish) {
    return <div>Желание не найдено</div>
  }

  return (
    <div className="min-h-screen bg-telegram-bg">
      <div className="p-4">
        <button onClick={() => navigate(-1)} className="text-telegram-link mb-4">
          ← Назад
        </button>
      </div>

      {wish.image_url && (
        <img
          src={wish.image_url}
          alt={wish.title}
          className="w-full h-64 object-cover"
        />
      )}

      <div className="p-4">
        <h1 className="text-2xl font-bold text-telegram-text mb-2">
          {wish.title}
        </h1>

        {wish.price && (
          <p className="text-xl font-bold text-telegram-button mb-4">
            {wish.price} {wish.currency}
          </p>
        )}

        {wish.description && (
          <p className="text-telegram-text mb-4">{wish.description}</p>
        )}

        {wish.link && (
          <a
            href={wish.link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-telegram-link block mb-4"
          >
            🔗 Открыть ссылку
          </a>
        )}

        <div className="space-y-3 mt-6">
          <button
            onClick={() => completeMutation.mutate()}
            disabled={wish.status === 'completed'}
            className="w-full bg-green-500 text-white py-3 rounded-lg font-medium hover:bg-green-600 transition disabled:opacity-50"
          >
            ✅ Отметить как выполненное
          </button>

          <button
            onClick={() => {
              if (confirm('Удалить это желание?')) {
                deleteMutation.mutate()
              }
            }}
            className="w-full bg-red-500 text-white py-3 rounded-lg font-medium hover:bg-red-600 transition"
          >
            🗑 Удалить
          </button>
        </div>
      </div>
    </div>
  )
}
