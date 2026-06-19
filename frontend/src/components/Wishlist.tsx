import { useEffect, useState } from 'react'
import { api, isAdmin, type WishlistItem } from '../api/client'

function formatPrice(v: number): string {
  return v.toLocaleString('pl-PL', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' zł'
}

export default function Wishlist() {
  const [items, setItems] = useState<WishlistItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')

  // add form
  const [formOpen, setFormOpen] = useState(false)
  const [name, setName] = useState('')
  const [planszeoUrl, setPlanszeoUrl] = useState('')
  const [bggUrl, setBggUrl] = useState('')
  const [notes, setNotes] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  // per-item refresh state
  const [refreshing, setRefreshing] = useState<Record<number, boolean>>({})
  const [refreshError, setRefreshError] = useState<Record<number, string>>({})
  const admin = isAdmin()

  useEffect(() => {
    api.wishlist.list()
      .then(setItems)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault()
    if (!name.trim()) return
    setSubmitting(true)
    setFormError(null)
    try {
      const item = await api.wishlist.create({
        name: name.trim(),
        planszeo_url: planszeoUrl.trim() || null,
        bgg_url: bggUrl.trim() || null,
        notes: notes.trim() || null,
      })
      setItems(prev => [item, ...prev])
      setName(''); setPlanszeoUrl(''); setBggUrl(''); setNotes('')
      setFormOpen(false)
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Błąd')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleRefresh(id: number) {
    setRefreshing(prev => ({ ...prev, [id]: true }))
    setRefreshError(prev => ({ ...prev, [id]: '' }))
    try {
      const updated = await api.wishlist.refreshPrice(id)
      setItems(prev => prev.map(it => it.id === id ? updated : it))
    } catch (err) {
      setRefreshError(prev => ({ ...prev, [id]: err instanceof Error ? err.message : 'Błąd' }))
    } finally {
      setRefreshing(prev => ({ ...prev, [id]: false }))
    }
  }

  async function handleDelete(id: number) {
    if (!confirm('Usunąć z listy życzeń?')) return
    await api.wishlist.delete(id)
    setItems(prev => prev.filter(it => it.id !== id))
  }

  if (loading) return <p className="status">Ładowanie...</p>
  if (error) return <p className="status error">Błąd: {error}</p>

  const q = search.trim().toLowerCase()
  const visible = q ? items.filter(it => it.name.toLowerCase().includes(q)) : items

  return (
    <section className="wishlist">
      <div className="detail-card-header" style={{ marginBottom: '1rem' }}>
        <h2>Lista życzeń ({items.length})</h2>
        {admin && !formOpen && <button onClick={() => setFormOpen(true)}>+ Dodaj grę</button>}
      </div>

      {formOpen && (
        <form className="add-game-form" onSubmit={handleAdd}>
          <h3>Nowa pozycja</h3>
          <div className="form-row">
            <input type="text" placeholder="Nazwa gry" value={name} onChange={e => setName(e.target.value)} required />
          </div>
          <div className="form-row" style={{ marginTop: '0.5rem' }}>
            <input type="url" placeholder="Link Planszeo (do oferty cenowej)" value={planszeoUrl} onChange={e => setPlanszeoUrl(e.target.value)} style={{ flex: 1 }} />
          </div>
          <div className="form-row" style={{ marginTop: '0.5rem' }}>
            <input type="url" placeholder="Link BGG (opcjonalnie)" value={bggUrl} onChange={e => setBggUrl(e.target.value)} style={{ flex: 1 }} />
          </div>
          <div className="form-row" style={{ marginTop: '0.5rem' }}>
            <input type="text" placeholder="Notatki (opcjonalnie)" value={notes} onChange={e => setNotes(e.target.value)} style={{ flex: 1 }} />
          </div>
          {formError && <p className="form-error">{formError}</p>}
          <div className="form-row" style={{ marginTop: '0.75rem' }}>
            <button type="submit" disabled={submitting}>{submitting ? 'Dodawanie...' : 'Dodaj'}</button>
            <button type="button" className="btn-cancel" onClick={() => setFormOpen(false)}>Anuluj</button>
          </div>
        </form>
      )}

      <input
        type="search"
        className="search-input"
        placeholder="Szukaj gry..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      {visible.length === 0 ? (
        <p className="status">Lista życzeń pusta</p>
      ) : (
        <ul className="wishlist-list">
          {visible.map(item => (
            <li key={item.id} className="wishlist-card">
              <div className="wishlist-main">
                <span className="wishlist-name">{item.name}</span>
                {item.notes && <p className="wishlist-notes">{item.notes}</p>}
                <div className="wishlist-links">
                  {item.planszeo_url && <a href={item.planszeo_url} target="_blank" rel="noopener noreferrer" className="bgg-link">Planszeo ↗</a>}
                  {item.bgg_url && <a href={item.bgg_url} target="_blank" rel="noopener noreferrer" className="bgg-link">BGG ↗</a>}
                </div>
              </div>

              <div className="wishlist-price-box">
                {item.best_price != null ? (
                  <>
                    <span className="wishlist-price">{formatPrice(item.best_price)}</span>
                    <span className="wishlist-price-meta">
                      {item.best_price_shop ?? '—'}{item.offer_count ? ` · ${item.offer_count} ofert` : ''}
                    </span>
                    {item.price_updated_at && (
                      <span className="wishlist-price-date">{new Date(item.price_updated_at).toLocaleString('pl-PL')}</span>
                    )}
                  </>
                ) : (
                  <span className="wishlist-price-meta">brak ceny</span>
                )}
                {admin && (
                  <div className="wishlist-actions">
                    <button
                      className="btn-bgg-search"
                      onClick={() => handleRefresh(item.id)}
                      disabled={!item.planszeo_url || refreshing[item.id]}
                      title={item.planszeo_url ? 'Pobierz najtańszą cenę z Planszeo' : 'Dodaj link Planszeo aby pobrać cenę'}
                    >{refreshing[item.id] ? '...' : '⟳ cena'}</button>
                    <button className="btn-delete" onClick={() => handleDelete(item.id)} title="Usuń">×</button>
                  </div>
                )}
                {refreshError[item.id] && <span className="form-error" style={{ fontSize: '0.75rem' }}>{refreshError[item.id]}</span>}
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
