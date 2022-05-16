import { FC } from 'react'

export interface ValidationMessageProps {
  message: string
}

export const ValidationMessage: FC<ValidationMessageProps> = ({ message }) => {
  return <div style={{ color: '#f11a30', fontSize: '13px' }}>{message}</div>
}
