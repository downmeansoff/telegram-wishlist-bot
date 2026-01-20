import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQueryClient } from 'react-query'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { wishesAPI } from '@/services/api'
import { WishPriority } from '@/types'

interface WishForm {
  title: string
  description?: string
  link?: string
  price?: number
  currency: string
  priority: WishPriority
}

export default function AddWishPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { register, handleSubmit, formState: { errors } } = useForm<WishForm>({
    defaultValues: {
      currency: 'RUB',
      priority: WishPriority.MEDIUM,
    },
  })

  const createMutation = useMutation(
    (data: WishForm) => wishesAPI.createWish(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('wishes')
        queryClient.invalidateQueries('profile')
        toast.success('Желание добавлено! 🎉')
        navigate('/wishes')
      },
      onError: () => {
        toast.error('Ошибка при добавлении')
      },
    }
  )

  const onSubmit = (data: WishForm) => {
    createMutation.mutate(data)
  }

  return (
    <div className="min-h-screen bg-telegram-bg p-4">
      <div className="max-w-lg mx-auto">
        <div className="mb-6">
          <button
            onClick={() => navigate(-1)}
            className="text-telegram-link mb-4"
          >
            ← Назад
          </button>
          <h1 className="text-2xl font-bold text-telegram-text">
            ➕ Добавить желание
          </h1>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-telegram-text mb-2">
              Название *
            </label>
            <input
              {...register('title', { required: 'Обязательное поле' })}
              className="w-full px-4 py-3 rounded-lg bg-telegram-secondaryBg text-telegram-text border-none focus:outline-none focus:ring-2 focus:ring-telegram-button"
              placeholder="iPhone 15 Pro"
            />
            {errors.title && (
              <p className="text-red-500 text-sm mt-1">{errors.title.message}</p>
            )}
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-telegram-text mb-2">
              Описание
            </label>
            <textarea
              {...register('description')}
              rows={3}
              className="w-full px-4 py-3 rounded-lg bg-telegram-secondaryBg text-telegram-text border-none focus:outline-none focus:ring-2 focus:ring-telegram-button resize-none"
              placeholder="Подробное описание..."
            />
          </div>

          {/* Link */}
          <div>
            <label className="block text-sm font-medium text-telegram-text mb-2">
              Ссылка
            </label>
            <input
              {...register('link')}
              type="url"
              className="w-full px-4 py-3 rounded-lg bg-telegram-secondaryBg text-telegram-text border-none focus:outline-none focus:ring-2 focus:ring-telegram-button"
              placeholder="https://..."
            />
          </div>

          {/* Price */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-telegram-text mb-2">
                Цена
              </label>
              <input
                {...register('price', { valueAsNumber: true })}
                type="number"
                step="0.01"
                className="w-full px-4 py-3 rounded-lg bg-telegram-secondaryBg text-telegram-text border-none focus:outline-none focus:ring-2 focus:ring-telegram-button"
                placeholder="0"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-telegram-text mb-2">
                Валюта
              </label>
              <select
                {...register('currency')}
                className="w-full px-4 py-3 rounded-lg bg-telegram-secondaryBg text-telegram-text border-none focus:outline-none focus:ring-2 focus:ring-telegram-button"
              >
                <option value="RUB">₽ RUB</option>
                <option value="USD">$ USD</option>
                <option value="EUR">€ EUR</option>
              </select>
            </div>
          </div>

          {/* Priority */}
          <div>
            <label className="block text-sm font-medium text-telegram-text mb-2">
              Приоритет
            </label>
            <div className="grid grid-cols-4 gap-2">
              {[
                { value: 1, label: '🟢 Низкий', color: 'bg-green-100' },
                { value: 2, label: '🟡 Средний', color: 'bg-yellow-100' },
                { value: 3, label: '🔴 Высокий', color: 'bg-orange-100' },
                { value: 4, label: '⚡ Срочный', color: 'bg-red-100' },
              ].map((priority) => (
                <label key={priority.value} className="cursor-pointer">
                  <input
                    {...register('priority')}
                    type="radio"
                    value={priority.value}
                    className="sr-only peer"
                  />
                  <div className="p-3 text-center rounded-lg bg-telegram-secondaryBg peer-checked:ring-2 peer-checked:ring-telegram-button transition">
                    <div className="text-2xl mb-1">{priority.label.split(' ')[0]}</div>
                    <div className="text-xs text-telegram-hint">
                      {priority.label.split(' ')[1]}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={createMutation.isLoading}
            className="w-full bg-telegram-button text-telegram-buttonText py-3 rounded-lg font-medium hover:opacity-80 transition disabled:opacity-50"
          >
            {createMutation.isLoading ? 'Добавление...' : 'Добавить желание'}
          </button>
        </form>
      </div>
    </div>
  )
}
