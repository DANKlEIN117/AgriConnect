import Navbar from "./Navbar"
import Footer from "./Footer"

export default function Layout({ children }) {
    return (
        <div className="flex flex-col min-h-screen bg-gray-100 text-gray-800 font-sans">
            <Navbar />
            <main className="flex-1 p-6">{children}</main>
            <Footer />
        </div>
    )
}
