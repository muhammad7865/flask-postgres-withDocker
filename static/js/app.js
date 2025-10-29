document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm')
  const registerForm = document.getElementById('registerForm')
  const logoutBtn = document.getElementById('logoutBtn')

  // Handle Login
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault()
      const data = Object.fromEntries(new FormData(loginForm))
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      const result = await res.json()
      alert(result.message || 'Login successful')
      if (res.ok) window.location.href = '/dashboard'
    })
  }

  // Handle Register
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault()
      const data = Object.fromEntries(new FormData(registerForm))
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      const result = await res.json()
      alert(result.message || 'Account created')
      if (res.ok) window.location.href = '/login'
    })
  }

  // Dashboard data fetch
  if (window.location.pathname === '/dashboard') {
    fetch('/api/user/me')
      .then((res) => res.json())
      .then((data) => {
        document.getElementById('username').textContent =
          data.username || 'User'
        document.getElementById('email').textContent = data.email || 'N/A'
        document.getElementById('user_id').textContent = data.id || '-'
      })
  }

  // Logout
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      await fetch('/api/auth/logout', { method: 'POST' })
      window.location.href = '/'
    })
  }
})
