import { render, screen } from '@testing-library/react'
import App from './App'

test('renders AI Dev Agent Interface header', () => {
  render(<App />)
  const headerElement = screen.getByText(/AI Dev Agent Interface/i)
  expect(headerElement).toBeInTheDocument()
})
