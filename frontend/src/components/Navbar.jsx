export default function Navbar() {
    return (
        <nav className="sticky top-0 z-50 bg-white shadow-md">
            <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                <h1 className="text-2xl font-bold text-green-600">AgriConnect</h1>
                <ul className="flex gap-6 text-gray-700 font-medium">
                    <li><a href="#" className="hover:text-green-600 transition">Home</a></li>
                    <li><a href="#" className="hover:text-green-600 transition">Farmers</a></li>
                    <li><a href="#" className="hover:text-green-600 transition">Cooperatives</a></li>
                    <li><a href="#" className="hover:text-green-600 transition">Markets</a></li>
                </ul>
            </div>
        </nav>
    )
}
