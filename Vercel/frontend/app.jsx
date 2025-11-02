const { useState, useEffect } = React;

const API_URL = '/api';

axios.interceptors.request.use(function (config) {
    const user = window.currentUser;
    if (user && user.uid) {
        config.headers['X-User-ID'] = user.uid;
    }
    return config;
}, function (error) {
    return Promise.reject(error);
});

function App() {
    const [currentView, setCurrentView] = useState('dashboard');
    const [notification, setNotification] = useState(null);
    const [confirmDialog, setConfirmDialog] = useState(null);

    const showNotification = (message, type = 'info') => {
        setNotification({ message, type });
        setTimeout(() => setNotification(null), 3000);
    };

    const showConfirm = (message, onConfirm) => {
        setConfirmDialog({ message, onConfirm });
    };

    return (
        <div className="app-container">
            <Navbar currentView={currentView} setCurrentView={setCurrentView} />
            <MainContent 
                currentView={currentView} 
                showNotification={showNotification}
                showConfirm={showConfirm}
            />
            {notification && (
                <Notification 
                    message={notification.message} 
                    type={notification.type}
                    onClose={() => setNotification(null)}
                />
            )}
            {confirmDialog && (
                <ConfirmDialog
                    message={confirmDialog.message}
                    onConfirm={() => {
                        confirmDialog.onConfirm();
                        setConfirmDialog(null);
                    }}
                    onCancel={() => setConfirmDialog(null)}
                />
            )}
        </div>
    );
}

function Notification({ message, type, onClose }) {
    return (
        <div className={`notification notification-${type}`} onClick={onClose}>
            <span>{message}</span>
            <button className="notification-close" onClick={onClose}>×</button>
        </div>
    );
}

function ConfirmDialog({ message, onConfirm, onCancel }) {
    return (
        <div className="modal-overlay" onClick={onCancel}>
            <div className="modal confirm-dialog" onClick={(e) => e.stopPropagation()}>
                <h3 className="confirm-title">Confirm Action</h3>
                <p className="confirm-message">{message}</p>
                <div className="confirm-actions">
                    <button className="btn btn-danger" onClick={onConfirm}>Yes, Delete</button>
                    <button className="btn btn-secondary" onClick={onCancel}>Cancel</button>
                </div>
            </div>
        </div>
    );
}

function Navbar({ currentView, setCurrentView }) {
    const menuItems = [
        { id: 'dashboard', icon: '📊', label: 'Dashboard' },
        { id: 'sweets', icon: '🍬', label: 'Sweets' },
        { id: 'customers', icon: '👥', label: 'Customers' },
        { id: 'orders', icon: '📦', label: 'Orders' }
    ];

    const userName = window.currentUser?.displayName || window.currentUser?.email || 'User';

    return (
        <nav className="navbar">
            <div className="nav-content">
                <div className="brand">
                    <div className="brand-logo">🪔</div>
                    <div className="brand-text">
                        <h1>Mithai Mandir</h1>
                        <p>PREMIUM INDIAN SWEETS</p>
                    </div>
                </div>
                <ul className="nav-menu">
                    {menuItems.map(item => (
                        <li
                            key={item.id}
                            className={`nav-item ${currentView === item.id ? 'active' : ''}`}
                            onClick={() => setCurrentView(item.id)}
                        >
                            <span>{item.icon}</span>
                            <span>{item.label}</span>
                        </li>
                    ))}
                </ul>
                <div className="nav-user">
                    <span className="user-name">{userName}</span>
                    <button className="btn-logout" onClick={() => window.handleLogout()}>
                        Logout
                    </button>
                </div>
            </div>
        </nav>
    );
}

function MainContent({ currentView, showNotification, showConfirm }) {
    return (
        <>
            {currentView === 'dashboard' && <Dashboard showNotification={showNotification} />}
            {currentView === 'sweets' && <Sweets showNotification={showNotification} showConfirm={showConfirm} />}
            {currentView === 'customers' && <Customers showNotification={showNotification} showConfirm={showConfirm} />}
            {currentView === 'orders' && <Orders showNotification={showNotification} showConfirm={showConfirm} />}
        </>
    );
}

function Dashboard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const response = await axios.get(`${API_URL}/dashboard/stats`);
            setStats(response.data);
        } catch (error) {
            console.error('Error fetching stats:', error);
            // Set default stats if API fails
            setStats({
                total_sweets: 0,
                total_customers: 0,
                total_orders: 0,
                total_revenue: 0
            });
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="loading">Loading dashboard</div>;

    return (
        <>
            <div className="hero-section">
                <div className="hero-content">
                    <h2>Welcome to Mithai Mandir</h2>
                    <p>Bringing Traditional Indian Sweets to Your Doorstep</p>
                </div>
            </div>
            <div className="main-content">
                <div className="dashboard-grid">
                    <div className="stat-card">
                        <span className="stat-icon">🍬</span>
                        <div className="stat-label">Total Sweets</div>
                        <div className="stat-value">{stats?.total_sweets || 0}</div>
                    </div>
                    <div className="stat-card">
                        <span className="stat-icon">👥</span>
                        <div className="stat-label">Total Customers</div>
                        <div className="stat-value">{stats?.total_customers || 0}</div>
                    </div>
                    <div className="stat-card">
                        <span className="stat-icon">📦</span>
                        <div className="stat-label">Total Orders</div>
                        <div className="stat-value">{stats?.total_orders || 0}</div>
                    </div>
                    <div className="stat-card">
                        <span className="stat-icon">💰</span>
                        <div className="stat-label">Total Revenue</div>
                        <div className="stat-value">₹{stats?.total_revenue?.toFixed(2) || '0.00'}</div>
                    </div>
                </div>
            </div>
        </>
    );
}

function Sweets({ showNotification, showConfirm }) {
    const [sweets, setSweets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [showModal, setShowModal] = useState(false);
    const [editingSweet, setEditingSweet] = useState(null);

    useEffect(() => {
        fetchSweets();
    }, []);

    const fetchSweets = async () => {
        try {
            const response = await axios.get(`${API_URL}/sweets`);
            setSweets(Array.isArray(response.data) ? response.data : []);
        } catch (error) {
            console.error('Error fetching sweets:', error);
            setSweets([]);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        showConfirm('Are you sure you want to delete this sweet?', async () => {
            try {
                await axios.delete(`${API_URL}/sweets/${id}`);
                fetchSweets();
                showNotification('Sweet deleted successfully', 'success');
            } catch (error) {
                console.error('Error deleting sweet:', error);
                const errorMsg = error.response?.data?.error || 'Failed to delete sweet';
                showNotification(errorMsg, 'error');
            }
        });
    };

    const filteredSweets = sweets.filter(sweet =>
        sweet.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        sweet.category.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) return <div className="loading">Loading sweets collection</div>;

    return (
        <div className="main-content">
            <div className="section-header">
                <h2 className="section-title">Our Sweet Collection</h2>
            </div>
            <div className="search-bar">
                <input
                    type="text"
                    className="search-input"
                    placeholder="🔍 Search for sweets..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <button className="btn btn-primary" onClick={() => { setEditingSweet(null); setShowModal(true); }}>
                    ➕ Add New Sweet
                </button>
            </div>

            {filteredSweets.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">🍬</div>
                    <h3 className="empty-state-title">No Sweets Found</h3>
                    <p className="empty-state-text">Start by adding your first sweet to the collection</p>
                    <button className="btn btn-primary" onClick={() => { setEditingSweet(null); setShowModal(true); }}>
                        ➕ Add Sweet
                    </button>
                </div>
            ) : (
                <div className="product-grid">
                    {filteredSweets.map(sweet => (
                        <div key={sweet.id} className="product-card">
                            <div className="product-image">
                                {sweet.image_url ? (
                                    <img src={sweet.image_url} alt={sweet.name} />
                                ) : (
                                    <span style={{ fontSize: '80px' }}>🍬</span>
                                )}
                                <div className="product-badge">{sweet.category}</div>
                            </div>
                            <div className="product-content">
                                <h3 className="product-name">{sweet.name}</h3>
                                <p className="product-description">{sweet.description || 'Delicious traditional Indian sweet'}</p>
                                <div className="product-meta">
                                    <div className="product-price">₹{sweet.price}</div>
                                    <div className="product-stock">
                                        <span className={sweet.stock > 10 ? 'badge badge-success' : sweet.stock > 0 ? 'badge badge-warning' : 'badge badge-danger'}>
                                            {sweet.stock} units
                                        </span>
                                    </div>
                                </div>
                                <div className="product-actions">
                                    <button className="btn btn-secondary btn-sm" onClick={() => { setEditingSweet(sweet); setShowModal(true); }}>
                                        ✏️ Edit
                                    </button>
                                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(sweet.id)}>
                                        🗑️ Delete
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {showModal && (
                <SweetModal
                    sweet={editingSweet}
                    onClose={() => { setShowModal(false); setEditingSweet(null); }}
                    onSuccess={() => {
                        fetchSweets();
                        setShowModal(false);
                        setEditingSweet(null);
                        showNotification(editingSweet ? 'Sweet updated successfully' : 'Sweet added successfully', 'success');
                    }}
                />
            )}
        </div>
    );
}

function SweetModal({ sweet, onClose, onSuccess }) {
    const [formData, setFormData] = useState({
        name: sweet?.name || '',
        category: sweet?.category || '',
        price: sweet?.price || '',
        stock: sweet?.stock || '',
        description: sweet?.description || '',
        image_url: sweet?.image_url || ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [imagePreview, setImagePreview] = useState(sweet?.image_url || '');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        if (name === 'image_url') {
            setImagePreview(value);
        }
    };

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setFormData({ ...formData, image_url: reader.result });
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (sweet) {
                await axios.put(`${API_URL}/sweets/${sweet.id}`, formData);
            } else {
                await axios.post(`${API_URL}/sweets`, formData);
            }
            onSuccess();
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to save sweet');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
                <h2 className="modal-title">{sweet ? 'Edit Sweet' : 'Add New Sweet'}</h2>
                {error && <div className="error">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Sweet Name</label>
                        <input type="text" name="name" className="form-input" value={formData.name} onChange={handleChange} required placeholder="e.g., Kaju Katli" />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Category</label>
                        <input type="text" name="category" className="form-input" value={formData.category} onChange={handleChange} required placeholder="e.g., Barfi, Ladoo, Halwa" />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Price (₹ per kg)</label>
                        <input type="number" step="0.01" name="price" className="form-input" value={formData.price} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Stock (kg)</label>
                        <input type="number" name="stock" className="form-input" value={formData.stock} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Description</label>
                        <textarea name="description" className="form-textarea" value={formData.description} onChange={handleChange} placeholder="Describe the sweet..."></textarea>
                    </div>
                    <div className="form-group">
                        <label className="form-label">Upload Image</label>
                        <input type="file" accept="image/*" className="form-input" onChange={handleImageUpload} />
                        <div style={{ marginTop: '12px' }}>
                            <label className="form-label">Or Enter Image URL</label>
                            <input type="text" name="image_url" className="form-input" placeholder="https://example.com/sweet.jpg" value={formData.image_url} onChange={handleChange} />
                        </div>
                        {imagePreview && (
                            <div className="image-preview-container">
                                <img src={imagePreview} alt="Preview" className="image-preview" onError={(e) => { e.target.style.display = 'none'; }} />
                            </div>
                        )}
                    </div>
                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? 'Saving...' : sweet ? 'Update Sweet' : 'Add Sweet'}
                        </button>
                        <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

function Customers({ showNotification, showConfirm }) {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [editingCustomer, setEditingCustomer] = useState(null);

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        try {
            const response = await axios.get(`${API_URL}/customers`);
            setCustomers(Array.isArray(response.data) ? response.data : []);
        } catch (error) {
            console.error('Error fetching customers:', error);
            setCustomers([]);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        showConfirm('Are you sure you want to delete this customer?', async () => {
            try {
                await axios.delete(`${API_URL}/customers/${id}`);
                fetchCustomers();
                showNotification('Customer deleted successfully', 'success');
            } catch (error) {
                const errorMsg = error.response?.data?.error || 'Failed to delete customer';
                showNotification(errorMsg, 'error');
            }
        });
    };

    if (loading) return <div className="loading">Loading customers</div>;

    return (
        <div className="main-content">
            <div className="section-header">
                <h2 className="section-title">Customer Management</h2>
                <button className="btn btn-primary" onClick={() => { setEditingCustomer(null); setShowModal(true); }}>
                    ➕ Add Customer
                </button>
            </div>
            <div className="content-card">
                {customers.length === 0 ? (
                    <div className="empty-state">
                        <div className="empty-state-icon">👥</div>
                        <h3 className="empty-state-title">No Customers Yet</h3>
                        <p className="empty-state-text">Add your first customer to get started</p>
                    </div>
                ) : (
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>Address</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {customers.map(customer => (
                                <tr key={customer.id}>
                                    <td>#{customer.id}</td>
                                    <td>{customer.name}</td>
                                    <td>{customer.email}</td>
                                    <td>{customer.phone || 'N/A'}</td>
                                    <td>{customer.address || 'N/A'}</td>
                                    <td>
                                        <button className="btn btn-secondary btn-sm" onClick={() => { setEditingCustomer(customer); setShowModal(true); }}>Edit</button>
                                        {' '}
                                        <button className="btn btn-danger btn-sm" onClick={() => handleDelete(customer.id)}>Delete</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
            {showModal && (
                <CustomerModal 
                    customer={editingCustomer} 
                    onClose={() => { setShowModal(false); setEditingCustomer(null); }} 
                    onSuccess={() => { 
                        fetchCustomers(); 
                        setShowModal(false); 
                        setEditingCustomer(null);
                        showNotification(editingCustomer ? 'Customer updated successfully' : 'Customer added successfully', 'success');
                    }} 
                />
            )}
        </div>
    );
}

function CustomerModal({ customer, onClose, onSuccess }) {
    const [formData, setFormData] = useState({
        name: customer?.name || '',
        email: customer?.email || '',
        phone: customer?.phone || '',
        address: customer?.address || ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (customer) {
                await axios.put(`${API_URL}/customers/${customer.id}`, formData);
            } else {
                await axios.post(`${API_URL}/customers`, formData);
            }
            onSuccess();
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to save customer');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
                <h2 className="modal-title">{customer ? 'Edit Customer' : 'Add New Customer'}</h2>
                {error && <div className="error">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Name</label>
                        <input type="text" name="name" className="form-input" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Email</label>
                        <input type="email" name="email" className="form-input" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} required />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Phone</label>
                        <input type="tel" name="phone" className="form-input" value={formData.phone} onChange={(e) => setFormData({ ...formData, phone: e.target.value })} />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Address</label>
                        <textarea name="address" className="form-textarea" value={formData.address} onChange={(e) => setFormData({ ...formData, address: e.target.value })}></textarea>
                    </div>
                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? 'Saving...' : 'Save Customer'}</button>
                        <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

function Orders({ showNotification, showConfirm }) {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [showStatusModal, setShowStatusModal] = useState(false);
    const [editingOrder, setEditingOrder] = useState(null);

    useEffect(() => {
        fetchOrders();
    }, []);

    const fetchOrders = async () => {
        try {
            const response = await axios.get(`${API_URL}/orders`);
            setOrders(Array.isArray(response.data) ? response.data : []);
        } catch (error) {
            console.error('Error fetching orders:', error);
            setOrders([]);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        showConfirm('Are you sure? This will restore inventory.', async () => {
            try {
                await axios.delete(`${API_URL}/orders/${id}`);
                fetchOrders();
                showNotification('Order deleted successfully', 'success');
            } catch (error) {
                showNotification('Failed to delete order', 'error');
            }
        });
    };

    const getStatusBadge = (status) => {
        const badges = { pending: 'badge-warning', completed: 'badge-success', cancelled: 'badge-danger' };
        return `badge ${badges[status] || 'badge-warning'}`;
    };

    if (loading) return <div className="loading">Loading orders</div>;

    return (
        <div className="main-content">
            <div className="section-header">
                <h2 className="section-title">Order Management</h2>
                <button className="btn btn-primary" onClick={() => setShowModal(true)}>➕ Create Order</button>
            </div>
            <div className="content-card">
                {orders.length === 0 ? (
                    <div className="empty-state">
                        <div className="empty-state-icon">📦</div>
                        <h3 className="empty-state-title">No Orders Yet</h3>
                        <p className="empty-state-text">Create your first order to get started</p>
                    </div>
                ) : (
                    <table>
                        <thead>
                            <tr>
                                <th>Order ID</th>
                                <th>Customer</th>
                                <th>Date</th>
                                <th>Status</th>
                                <th>Total</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {orders.map(order => (
                                <tr key={order.id}>
                                    <td>#{order.id}</td>
                                    <td>{order.customer?.name || 'N/A'}</td>
                                    <td>{new Date(order.order_date).toLocaleDateString('en-IN')}</td>
                                    <td><span className={getStatusBadge(order.status)}>{order.status}</span></td>
                                    <td>₹{order.total_price?.toFixed(2) || '0.00'}</td>
                                    <td>
                                        <button className="btn btn-secondary btn-sm" onClick={() => { setEditingOrder(order); setShowStatusModal(true); }}>📝 Status</button>
                                        {' '}
                                        <button className="btn btn-danger btn-sm" onClick={() => handleDelete(order.id)}>Delete</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
            {showStatusModal && <StatusModal order={editingOrder} onClose={() => { setShowStatusModal(false); setEditingOrder(null); }} onSuccess={() => { fetchOrders(); setShowStatusModal(false); setEditingOrder(null); showNotification('Order status updated', 'success'); }} />}
            {showModal && <OrderModal onClose={() => setShowModal(false)} onSuccess={() => { fetchOrders(); setShowModal(false); showNotification('Order created successfully', 'success'); }} />}
        </div>
    );
}

function StatusModal({ order, onClose, onSuccess }) {
    const [status, setStatus] = useState(order?.status || 'pending');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await axios.put(`${API_URL}/orders/${order.id}`, { status });
            onSuccess();
        } catch (err) {
            setError('Failed to update status');
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '400px' }}>
                <h2 className="modal-title">Update Order Status</h2>
                <p style={{ color: 'var(--text-light)', marginBottom: '20px' }}>Order #{order.id} - {order.customer?.name}</p>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Status</label>
                        <select className="form-select" value={status} onChange={(e) => setStatus(e.target.value)} required>
                            <option value="pending">Pending</option>
                            <option value="completed">Completed</option>
                            <option value="cancelled">Cancelled</option>
                        </select>
                    </div>
                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? 'Updating...' : 'Update'}</button>
                        <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

function OrderModal({ onClose, onSuccess }) {
    const [customers, setCustomers] = useState([]);
    const [sweets, setSweets] = useState([]);
    const [formData, setFormData] = useState({ customer_id: '', items: [] });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        axios.get(`${API_URL}/customers`)
            .then(res => setCustomers(Array.isArray(res.data) ? res.data : []))
            .catch(err => { console.error(err); setCustomers([]); });
        axios.get(`${API_URL}/sweets`)
            .then(res => setSweets(Array.isArray(res.data) ? res.data : []))
            .catch(err => { console.error(err); setSweets([]); });
    }, []);

    const addItem = () => setFormData({ ...formData, items: [...formData.items, { sweet_id: '', quantity: 1 }] });
    const updateItem = (index, field, value) => {
        const newItems = [...formData.items];
        newItems[index][field] = field === 'quantity' ? parseInt(value) || 1 : value;
        setFormData({ ...formData, items: newItems });
    };
    const removeItem = (index) => setFormData({ ...formData, items: formData.items.filter((_, i) => i !== index) });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await axios.post(`${API_URL}/orders`, {
                customer_id: parseInt(formData.customer_id),
                items: formData.items.map(item => ({ sweet_id: parseInt(item.sweet_id), quantity: parseInt(item.quantity) }))
            });
            onSuccess();
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to create order');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
                <h2 className="modal-title">Create New Order</h2>
                {error && <div className="error">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Customer</label>
                        <select className="form-select" value={formData.customer_id} onChange={(e) => setFormData({ ...formData, customer_id: e.target.value })} required>
                            <option value="">Select Customer</option>
                            {customers.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                        </select>
                    </div>
                    <div className="form-group">
                        <label className="form-label">Order Items</label>
                        {formData.items.map((item, index) => (
                            <div key={index} style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                                <select className="form-select" value={item.sweet_id} onChange={(e) => updateItem(index, 'sweet_id', e.target.value)} required>
                                    <option value="">Select Sweet</option>
                                    {sweets.map(s => <option key={s.id} value={s.id}>{s.name} - ₹{s.price}/kg</option>)}
                                </select>
                                <input type="number" className="form-input" placeholder="Qty (kg)" value={item.quantity} onChange={(e) => updateItem(index, 'quantity', e.target.value)} min="1" required style={{ width: '120px' }} />
                                <button type="button" className="btn btn-danger btn-sm" onClick={() => removeItem(index)}>Remove</button>
                            </div>
                        ))}
                        <button type="button" className="btn btn-secondary btn-sm" onClick={addItem}>➕ Add Item</button>
                    </div>
                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? 'Creating...' : 'Create Order'}</button>
                        <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

// This script only runs after auth is complete (window.currentUser is set)
console.log('app.jsx executing for user:', window.currentUser?.email);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);