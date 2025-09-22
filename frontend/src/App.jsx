import Layout from "./components/Layout"

function App() {
  return (
    <Layout>
      <div className="max-w-3xl mx-auto text-center mt-10">
        <h2 className="text-4xl font-extrabold text-green-700">
          Welcome to AgriConnect 🌍
        </h2>
        <p className="mt-4 text-lg text-gray-600">
          Connecting farmers with cooperatives and markets — for better trade, fair prices, and growth.
        </p>
        <button className="mt-6 px-6 py-3 bg-green-600 text-white rounded-xl shadow hover:bg-green-700 transition">
          Get Started
        </button>
      </div>
    </Layout>
  )
}

export default App
