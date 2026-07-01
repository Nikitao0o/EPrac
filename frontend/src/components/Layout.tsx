import { useEffect, useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { getHealth } from '../api/client'

export function Layout() {
  const [apiStatus, setApiStatus] = useState<'loading' | 'ok' | 'error'>('loading')

  useEffect(() => {
    getHealth()
      .then(() => setApiStatus('ok'))
      .catch(() => setApiStatus('error'))
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header__inner">
          <div>
            <p className="app-header__eyebrow">EPrac</p>
            <h1 className="app-header__title">Поиск по документам</h1>
          </div>
          <span className={`status-badge status-badge--${apiStatus}`}>
            {apiStatus === 'loading' && 'Проверка API…'}
            {apiStatus === 'ok' && 'API доступен'}
            {apiStatus === 'error' && 'API недоступен'}
          </span>
        </div>
      </header>

      <nav className="app-nav">
        <div className="app-nav__inner">
          <NavLink
            to="/upload"
            className={({ isActive }) => `app-nav__link${isActive ? ' app-nav__link--active' : ''}`}
          >
            Загрузка
          </NavLink>
          <NavLink
            to="/search"
            className={({ isActive }) => `app-nav__link${isActive ? ' app-nav__link--active' : ''}`}
          >
            Поиск
          </NavLink>
        </div>
      </nav>

      <main className="app-main">
        <Outlet />
      </main>
    </div>
  )
}
