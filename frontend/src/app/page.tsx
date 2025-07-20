// 'use client'
// import { useEffect, useState } from "react";
// import Image from "next/image";
// import Link from 'next/link';

// import NavbarCom from "@/components/NavbarCom";
// import TopNavbarCom from "@/components/TopNavbarCom";
// import FooterCom from "@/components/FooterCom";
// import ContentpageHome from "@/components/ContentpageHome";
// import AdModal from "@/components/AdModal";
// import BannerSliderHomeCom from "@/components/BannerSliderHomeCom";

// export default function Home() {
//   const [message, setMessage] = useState("");

//   useEffect(() => {
//     // Fetch data from FastAPI backend
//     fetch("http://localhost:8000/api/hello")
//       .then((res) => res.json())
//       .then((data) => setMessage(data.message))
//       .catch((err) => console.error("FastAPI Error:", err));
//   }, []);

//   return (
//     <div className="bg-gray-50">
//       <AdModal />
//       <TopNavbarCom />
//       <NavbarCom />
//       <BannerSliderHomeCom />

//       {/* ✅ Show response from FastAPI here */}
//       {message && (
//         <div className="text-center text-lg font-semibold text-blue-600 my-4">
//           {message}
//         </div>
//       )}

      
//       <FooterCom />
//     </div>
//   );
// }





'use client';
import { useEffect, useState } from "react";
import Image from "next/image";
import Link from 'next/link';

import NavbarCom from "@/components/NavbarCom";
import TopNavbarCom from "@/components/TopNavbarCom";
import FooterCom from "@/components/FooterCom";
import ContentpageHome from "@/components/ContentpageHome";
import AdModal from "@/components/AdModal";
import BannerSliderHomeCom from "@/components/BannerSliderHomeCom";

export default function Home() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/hello")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => console.error("FastAPI Error:", err));
  }, []);

  return (
    <div className="bg-gradient-to-br from-gray-100 via-white to-gray-50 min-h-screen font-sans">
      <AdModal />
      <TopNavbarCom />
      <NavbarCom />
      <BannerSliderHomeCom />

      {message && (
        <div className="text-center text-xl font-bold text-[#003366] mt-8 mb-6">
          {message}
        </div>
      )}

      {/* Luxury Intro Section */}
      <section className="max-w-7xl mx-auto px-6 py-12">
        <div className="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-10 border border-gray-200">
          <h1 className="text-4xl font-extrabold text-center text-gray-800 mb-4">
            Welcome to Elite HR Management
          </h1>
          <p className="text-lg text-center text-gray-600 max-w-2xl mx-auto">
            Empower your workforce with our modern, efficient, and elegantly designed HRM solution tailored to bring productivity and harmony.
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-6 py-12 grid md:grid-cols-3 gap-8">
        {[
          { title: "Smart Employee Dashboard", icon: "/images/dashboard.png" },
          { title: "Performance Reviews", icon: "/images/performance.png" },
          { title: "Automated Payroll", icon: "/images/payroll.png" },
        ].map((item, index) => (
          <div key={index} className="bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition duration-300 border border-gray-100">
            <Image
              src={item.icon}
              alt={item.title}
              width={60}
              height={60}
              className="mx-auto mb-4"
            />
            <h3 className="text-xl font-semibold text-gray-800 text-center mb-2">
              {item.title}
            </h3>
            <p className="text-sm text-gray-500 text-center">
              Streamline and elevate your operations with modern HR solutions.
            </p>
          </div>
        ))}
      </section>

      {/* Call to Action */}
      <section className="bg-gradient-to-r from-[#0f2027] via-[#203a43] to-[#2c5364] py-12 text-white text-center">
        <h2 className="text-3xl font-bold mb-4">Ready to modernize your HR?</h2>
        <p className="mb-6">Get started today and bring luxury and efficiency to your workforce.</p>
        <Link
          href="/signup"
          className="inline-block bg-white text-[#203a43] font-semibold py-2 px-6 rounded-full shadow hover:bg-gray-100 transition duration-300"
        >
          Get Started
        </Link>
      </section>

      <FooterCom />
    </div>
  );
}
