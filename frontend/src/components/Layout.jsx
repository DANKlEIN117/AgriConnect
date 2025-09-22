function Layout({ children }) {
    return (
        <div className="min-h-screen bg-gray-100 text-gray-900">
            {/* Navbar goes here */}
            {children}
        </div>
    );
}

export default Layout;
