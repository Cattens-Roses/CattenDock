import { useEffect, useState } from 'react'

const api = (path, opts) => fetch(`/api${path}`, opts).then(r => {
  if (!r.ok) throw new Error(r.statusText)
  return r.json()
})

export default function App() {
  const [stats, setStats] = useState(null)
  const [containers, setContainers] = useState([])
  const [apps, setApps] = useState([])
  const [error, setError] = useState('')

  async function refresh() {
    try {
      const [s, c, a] = await Promise.all([
        api('/system/'),
        api('/containers/'),
        api('/catalog/'),
      ])
      setStats(s); setContainers(c); setApps(a); setError('')
    } catch (e) {
      setError(e.message)
    }
  }

  useEffect(() => { refresh(); const t = setInterval(refresh, 5000); return () => clearInterval(t) }, [])

  async function action(id, verb, method = 'POST') {
    try {
      await api(`/containers/${id}/${verb}`, { method })
      refresh()
    } catch (e) { alert(e.message) }
  }

  async function deploy(appId) {
    try {
      await api(`/catalog/${appId}/deploy`, { method: 'POST' })
      refresh()
    } catch (e) { alert(e.message) }
  }

  return (
    <div className="app">
      <header>
        <h1>🐈 CattenDock</h1>
        {stats && <span className="host">{stats.hostname}</span>}
      </header>

      {error && <div className="error">{error}</div>}

      {stats && (
        <section className="stats">
          <Stat label="CPU" value={`${stats.cpu_percent.toFixed(1)}%`} />
          <Stat label="RAM" value={`${stats.memory.percent.toFixed(1)}%`} />
          <Stat label="Disk" value={`${stats.disk.percent.toFixed(1)}%`} />
          <Stat label="Uptime" value={`${Math.floor(stats.uptime_seconds / 3600)}h`} />
        </section>
      )}

      <section>
        <h2>Containers</h2>
        <div className="grid">
          {containers.length === 0 && <p className="muted">No containers yet.</p>}
          {containers.map(c => (
            <div className="card" key={c.id}>
              <div className="row">
                <strong>{c.name}</strong>
                <span className={`badge ${c.status}`}>{c.status}</span>
              </div>
              <p className="muted">{c.image}</p>
              <div className="row">
                {c.status !== 'running' && <button onClick={() => action(c.id, 'start')}>Start</button>}
                {c.status === 'running' && <button onClick={() => action(c.id, 'stop')}>Stop</button>}
                <button className="danger" onClick={() => action(c.id, '', 'DELETE')}>Remove</button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>App Catalog</h2>
        <div className="grid">
          {apps.map(a => (
            <div className="card" key={a.id}>
              <div className="row">
                <strong>{a.name}</strong>
              </div>
              <p className="muted">{a.description}</p>
              <button onClick={() => deploy(a.id)}>Deploy</button>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

function Stat({ label, value }) {
  return (
    <div className="stat">
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
    </div>
  )
}
