export default function Navbar() {
    return (
        <nav className="bg-green-700 text-white shadow-md sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
                {/* Logo / Brand */}
                <h1 className="text-2xl font-bold tracking-wide">AgriConnect 🚜</h1>

                {/* Links */}
                <ul className="flex space-x-8 font-medium">
                    <li><a href="#" className="hover:text-yellow-300">Home</a></li>
                    <li><a href="#" className="hover:text-yellow-300">Products</a></li>
                    <li><a href="#" className="hover:text-yellow-300">Dashboard</a></li>
                    <li><a href="#" className="hover:text-yellow-300">Login</a></li>
                </ul>
            </div>
        </nav>
    );
}
