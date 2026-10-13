import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [selectedProduct, setSelectedProduct] = useState(null);

  const [adminProducts, setAdminProducts] = useState([]);

  const [pname, setPname] = useState("");
  const [pprice, setPprice] = useState("");
  const [pdesc, setPdesc] = useState("");
  const [pcat, setPcat] = useState("");

  const [amazonLink, setAmazonLink] = useState("");
  const [flipkartLink, setFlipkartLink] = useState("");

  // 🎤 Voice Input
  const handleVoice = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice not supported");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = (event) => {
      setQuestion(event.results[0][0].transcript);
    };
  };

  // 🔊 Voice Output
  let utterance;

  const speakAnswer = (text) => {
    if (!text) return;
    window.speechSynthesis.cancel();
    utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    window.speechSynthesis.speak(utterance);
  };

  const pauseSpeech = () => window.speechSynthesis.pause();
  const resumeSpeech = () => window.speechSynthesis.resume();
  const stopSpeech = () => window.speechSynthesis.cancel();

  // 📁 Upload CSV
  const handleUpload = async () => {
    if (!file) return alert("Select file");

    const formData = new FormData();
    formData.append("file", file);

    await axios.post("http://127.0.0.1:8000/upload", formData);
    alert("Uploaded ✅");
  };

  // ❓ Ask
  const handleAsk = async () => {
    if (!question) return alert("Ask something");

    let res;

    try {
      if (file) {
        res = await axios.get("http://127.0.0.1:8000/ask", {
          params: { question, filename: file.name },
        });
      } else {
        res = await axios.get("http://127.0.0.1:8000/ask-live", {
          params: { question },
        });
      }

      setAnswer(res.data.answer);
      speakAnswer(res.data.answer);
    } catch {
      alert("Error fetching results");
    }
  };

  // 🧑‍💼 ADD PRODUCT
  const handleAddProduct = async () => {
    try {
      if (!pname || !pprice || !pdesc || !pcat) {
        alert("Fill all fields");
        return;
      }

      await axios.post("http://127.0.0.1:8000/admin/add-product", {
        name: pname,
        price: String(pprice),
        desc: pdesc,
        category: pcat,
        amazon: amazonLink,
        flipkart: flipkartLink,
      });

      alert("Product Added ✅");

      setPname("");
      setPprice("");
      setPdesc("");
      setPcat("");
      setAmazonLink("");
      setFlipkartLink("");

      loadAdminProducts();
    } catch {
      alert("Error adding product ❌");
    }
  };

  // 📥 Load Admin Products
  const loadAdminProducts = async () => {
    const res = await axios.get("http://127.0.0.1:8000/admin/products");
    setAdminProducts(res.data.products);
  };

  useEffect(() => {
    loadAdminProducts();
  }, []);

  // 🔥 Convert AI answer → products
  const products = answer
    .split("\n")
    .filter((l) => l.includes("₹"))
    .map((item) => {
      const parts = item.split("₹");
      const name = parts[0]?.trim();
      const rest = parts[1]?.split(" - ");

      return {
        name,
        price: rest?.[0],
        desc: rest?.[1],
        image: `https://dummyimage.com/300x200/1e293b/38bdf8&text=${encodeURIComponent(
          name
        )}`,
      };
    });

  // 🔥 Filter Admin
  const filteredAdminProducts = adminProducts.filter((p) => {
    return (
      question.toLowerCase().includes(p.category.toLowerCase()) ||
      p.name.toLowerCase().includes(question.toLowerCase())
    );
  });

  // 🔗 LINKS
  const openAmazon = (p) => {
    const url =
      p?.amazon && p.amazon.startsWith("http")
        ? p.amazon
        : `https://www.amazon.in/s?k=${encodeURIComponent(p.name)}`;

    window.open(url, "_blank", "noopener,noreferrer");
  };

  const openFlipkart = (p) => {
    const url =
      p?.flipkart && p.flipkart.startsWith("http")
        ? p.flipkart
        : `https://www.flipkart.com/search?q=${encodeURIComponent(p.name)}`;

    window.open(url, "_blank", "noopener,noreferrer");
  };

  const openGoogle = (name) =>
    window.open(
      `https://www.google.com/search?q=${encodeURIComponent(name)}`,
      "_blank"
    );

  return (
    <div className="container">
      <h1>🎙️ AI Catalog Assistant</h1>

      {/* Upload */}
      <div className="card">
        <h3>Upload CSV</h3>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload</button>
      </div>

      {/* Ask */}
      <div className="card">
        <h3>Ask Question</h3>

        <div className="input-row">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask something..."
          />
          <button onClick={handleVoice}>🎤</button>
        </div>

        <button onClick={handleAsk}>Ask</button>
      </div>

      {/* Results */}
      <div className="card">
        <h3>Results</h3>

        <div className="product-container">
          {(filteredAdminProducts.length > 0
            ? filteredAdminProducts
            : adminProducts
          ).map((p, i) => (
            <div key={"admin" + i} className="product-card">
              <img
                src={`https://dummyimage.com/300x200/000/fff&text=${encodeURIComponent(
                  p.name
                )}`}
                alt={p.name}
                className="product-img"
              />
              <h4>{p.name}</h4>
              <p className="price">₹{p.price}</p>
              <p className="desc">{p.desc}</p>

              <div className="btn-group">
                <button onClick={(e) => { e.stopPropagation(); openAmazon(p); }}>
                  🛒 Amazon
                </button>

                <button onClick={(e) => { e.stopPropagation(); openFlipkart(p); }}>
                  🛍 Flipkart
                </button>
              </div>
            </div>
          ))}

          {/* AI PRODUCTS */}
          {products.map((p, i) => (
            <div
              key={i}
              className="product-card"
              onClick={() => setSelectedProduct(p)}
            >
              <img src={p.image} alt={p.name} className="product-img" />
              <h4>{p.name}</h4>
              <p className="price">₹{p.price}</p>
              <p className="desc">{p.desc}</p>

              <div className="btn-group">
                <button onClick={(e) => { e.stopPropagation(); openAmazon(p); }}>
                  🛒 Amazon
                </button>

                <button onClick={(e) => { e.stopPropagation(); openFlipkart(p); }}>
                  🛍 Flipkart
                </button>

                <button onClick={(e) => { e.stopPropagation(); openGoogle(p.name); }}>
                  🔍 Search
                </button>
              </div>
            </div>
          ))}
        </div>

        {products.length === 0 && <pre>{answer}</pre>}

        {answer && (
          <div className="controls">
            <button onClick={pauseSpeech}>⏸</button>
            <button onClick={resumeSpeech}>▶</button>
            <button onClick={stopSpeech}>⏹</button>
          </div>
        )}
      </div>

      {/* Admin Panel */}
      <div className="card">
        <h3>Admin Panel</h3>

        <input placeholder="Name" value={pname} onChange={(e) => setPname(e.target.value)} />
        <input placeholder="Price" value={pprice} onChange={(e) => setPprice(e.target.value)} />
        <input placeholder="Description" value={pdesc} onChange={(e) => setPdesc(e.target.value)} />
        <input placeholder="Category" value={pcat} onChange={(e) => setPcat(e.target.value)} />

        <input placeholder="Amazon Link" value={amazonLink} onChange={(e) => setAmazonLink(e.target.value)} />
        <input placeholder="Flipkart Link" value={flipkartLink} onChange={(e) => setFlipkartLink(e.target.value)} />

        <button onClick={handleAddProduct}>➕ Add Product</button>
      </div>

      {/* ✅ FIXED MODAL */}
      {selectedProduct && (
        <div className="modal" onClick={() => setSelectedProduct(null)}>
          <div className="modal-content">
            <h2>{selectedProduct.name}</h2>
            <p>₹{selectedProduct.price}</p>
            <p>{selectedProduct.desc}</p>

            <div className="btn-group">
              <button onClick={(e) => { e.stopPropagation(); openAmazon(selectedProduct); }}>
                Amazon
              </button>

              <button onClick={(e) => { e.stopPropagation(); openFlipkart(selectedProduct); }}>
                Flipkart
              </button>

              <button onClick={(e) => { e.stopPropagation(); openGoogle(selectedProduct.name); }}>
                Search
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;