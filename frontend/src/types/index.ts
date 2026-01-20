export interface User {
  id: number
  telegram_id: number
  username?: string
  first_name: string
  last_name?: string
  avatar_url?: string
  language_code: string
  birthday?: string
  is_active: boolean
  is_premium: boolean
  created_at: string
  updated_at?: string
}

export interface UserProfile extends User {
  wishes_count: number
  completed_wishes_count: number
  groups_count: number
}

export enum WishStatus {
  ACTIVE = 'active',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

export enum WishPriority {
  LOW = 1,
  MEDIUM = 2,
  HIGH = 3,
  URGENT = 4,
}

export interface Wish {
  id: number
  user_id: number
  category_id?: number
  title: string
  description?: string
  image_url?: string
  link?: string
  price?: number
  currency: string
  priority: WishPriority
  status: WishStatus
  order_index: number
  is_public: boolean
  notes?: string
  created_at: string
  updated_at?: string
  completed_at?: string
}

export interface Category {
  id: number
  name: string
  emoji?: string
  color: string
  description?: string
  created_at: string
}

export interface Group {
  id: number
  name: string
  description?: string
  avatar_url?: string
  creator_id: number
  invite_code: string
  is_active: boolean
  created_at: string
  updated_at?: string
}

export interface GroupWithMembers extends Group {
  member_count: number
}

export enum GroupRole {
  OWNER = 'owner',
  ADMIN = 'admin',
  MEMBER = 'member',
}

export interface GroupMember {
  id: number
  group_id: number
  user_id: number
  role: GroupRole
  joined_at: string
}
