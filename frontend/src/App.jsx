import Navbar from "./components/Navbar";


function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <main className="p-6">
        <h1 className="text-4xl font-bold text-green-700">
          Welcome to AgriConnect 🚜
        </h1>
        <p className="mt-2 text-lg text-gray-600">
          Connecting farmers, cooperatives, and buyers.
        </p>
      </main>
    </div>
  );
}

export default App;
