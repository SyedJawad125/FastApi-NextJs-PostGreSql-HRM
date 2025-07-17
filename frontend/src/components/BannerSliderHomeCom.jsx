// 'use client';
// import React, { useState, useEffect } from 'react';
// import Image from 'next/image';
// import { Carousel } from "react-responsive-carousel";
// import "react-responsive-carousel/lib/styles/carousel.min.css";
// import { FiSearch, FiHeart, FiShoppingBag, FiUser, FiMenu, FiChevronRight } from 'react-icons/fi';
// import { IoIosArrowForward, IoIosArrowBack } from 'react-icons/io';
// import Link from 'next/link';
// import AxiosInstance from "@/components/AxiosInstance";

// const HomePage = () => {
//   const [isMenuOpen, setIsMenuOpen] = useState(false);
//   const [searchQuery, setSearchQuery] = useState('');
//   const [banners, setBanners] = useState([]);

//   useEffect(() => {
//     const fetchImages = async () => {
//       try {
//         const res = await AxiosInstance.get('/images/publicimages?imagescategory=Bannerslider');
//         if (res && res.data && res.data.data) {
//           setBanners(res.data.data.data);
//         } else {
//           console.error('Unexpected response structure:', res);
//         }
//       } catch (error) {
//         console.error('Error fetching images:', error);
//       }
//     };

//     fetchImages();
//   }, []);

//   const luxuryCategories = [
//     { name: "Haute Couture", subcategories: ["Evening Gowns", "Bridal", "Custom Tailoring"] },
//     { name: "Fine Jewelry", subcategories: ["Diamond", "Platinum", "Limited Editions"] },
//     { name: "Luxury Watches", subcategories: ["Swiss", "Automatic", "Limited Edition"] },
//     { name: "Designer Handbags", subcategories: ["Limited Edition", "Exotic Leathers", "Iconic Styles"] },
//     { name: "High-End Tech", subcategories: ["Luxury Phones", "Executive Gadgets", "Custom Finishes"] },
//     { name: "Premium Fragrances", subcategories: ["Niche Perfumes", "Private Blends", "Limited Editions"] },
//     { name: "Luxury Home", subcategories: ["Designer Furniture", "Art Pieces", "Premium Linens"] },
//     { name: "Exclusive Experiences", subcategories: ["VIP Travel", "Private Events", "Personal Shopping"] }
//   ];

//   const featuredProducts = [
//     { id: 1, name: "Diamond Eternity Band", price: "$12,500" },
//     { id: 2, name: "Limited Edition Chronograph", price: "$28,900" },
//     { id: 3, name: "Designer Leather Tote", price: "$5,200" },
//     { id: 4, name: "Custom Tailored Suit", price: "$8,750" },
//     { id: 5, name: "Rare Perfume Collection", price: "$3,400" }
//   ];

//   const renderArrowPrev = (clickHandler, hasPrev, label) => (
//     <button 
//       onClick={clickHandler}
//       className="absolute left-0 z-10 p-2 bg-black bg-opacity-50 hover:bg-opacity-70 text-white rounded-r-lg"
//       style={{ top: '50%', transform: 'translateY(-50%)' }}
//     >
//       <IoIosArrowBack size={24} />
//     </button>
//   );

//   const renderArrowNext = (clickHandler, hasNext, label) => (
//     <button 
//       onClick={clickHandler}
//       className="absolute right-0 z-10 p-2 bg-black bg-opacity-50 hover:bg-opacity-70 text-white rounded-l-lg"
//       style={{ top: '50%', transform: 'translateY(-50%)' }}
//     >
//       <IoIosArrowForward size={24} />
//     </button>
//   );

//   return (
//     <div className="min-h-screen bg-gray-50">
//       {/* Mobile Menu */}
//       {isMenuOpen && (
//         <div className="bg-black text-white p-6 md:hidden">
//           <div className="space-y-4">
//             <div className="relative">
//               <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
//               <input
//                 type="text"
//                 placeholder="Search..."
//                 className="bg-gray-800 text-white pl-10 pr-4 py-2 rounded-full focus:outline-none w-full"
//               />
//             </div>
//             <nav className="flex flex-col space-y-3">
//               <a href="#" className="hover:text-gray-300 transition">New Arrivals</a>
//               <a href="#" className="hover:text-gray-300 transition">Collections</a>
//               <a href="#" className="hover:text-gray-300 transition">Shop</a>
//               <a href="#" className="hover:text-gray-300 transition">Contact</a>
//             </nav>
//           </div>
//         </div>
//       )}

//       {/* Main Content */}
//       <main className="container mx-auto px-4 py-8">
//         {/* Hero Carousel */}
//         <div className="mb-12 relative">
//           <Carousel
//             showThumbs={false}
//             autoPlay
//             infiniteLoop
//             interval={5000}
//             showStatus={false}
//             renderArrowPrev={renderArrowPrev}
//             renderArrowNext={renderArrowNext}
//             className="overflow-hidden rounded-lg shadow-xl"
//           >
//             {banners.map((banner, index) => (
//               <div key={index}>
//                 <img
//                   src={`http://localhost:8000${banner.image}`}
//                   alt={`Banner ${index + 1}`}
//                   className="w-full h-[70vh] object-cover mb-12"
//                 />
//                 <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
//                   <div className="text-center text-white px-8 max-w-2xl">
//                     <h2 className="text-4xl md:text-5xl font-serif font-bold mb-4">Exclusive Collection {index + 1}</h2>
//                     <p className="text-xl mb-6">Discover unparalleled craftsmanship and timeless elegance</p>
//                     <Link href="/publicproducts">
//                       <button className="bg-white text-black px-8 py-3 font-medium hover:bg-opacity-90 transition">
//                         SHOP NOW
//                       </button>
//                     </Link>
//                   </div>
//                 </div>
//               </div>
//             ))}
//           </Carousel>
//         </div>

//         {/* Luxury Categories
//         <section className="mb-16">
//           <h2 className="text-3xl font-serif text-gray-900 font-bold mb-8 text-center">Our Luxury Categories</h2>
//           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
//             {luxuryCategories.map((category, index) => (
//               <div key={index} className="group relative overflow-hidden rounded-lg shadow-lg h-64">
//                 <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black opacity-70 z-10"></div>
//                 <div className="absolute inset-0 flex items-end p-6 z-20">
//                   <div>
//                     <h3 className="text-white text-xl font-bold mb-2">{category.name}</h3>
//                     <div className="flex flex-wrap gap-2">
//                       {category.subcategories.map((sub, i) => (
//                         <span key={i} className="text-xs text-white bg-black bg-opacity-50 px-2 py-1 rounded">
//                           {sub}
//                         </span>
//                       ))}
//                     </div>
//                   </div>
//                 </div>
//                 <div className="w-full h-full bg-gray-200 group-hover:scale-105 transition-transform duration-500">
                  
//                   <div className="w-full h-full bg-gray-300"></div>
//                 </div>
//               </div>
//             ))}
//           </div>
//         </section> */}

//         {/* Featured Products */}
//         {/* <section className="mb-16">
//           <div className="flex justify-between items-center mb-8">
//             <h2 className="text-3xl font-serif font-bold">Curated Selections</h2>
//             <button className="flex items-center text-sm font-medium hover:underline">
//               View All <FiChevronRight className="ml-1" />
//             </button>
//           </div>
          
//           <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
//             {featuredProducts.map((product) => (
//               <div key={product.id} className="group relative">
//                 <div className="aspect-square overflow-hidden rounded-lg bg-gray-100">
                  
//                   <div className="w-full h-full bg-gray-300"></div>
//                 </div>
//                 <div className="mt-4">
//                   <h3 className="text-lg font-medium text-gray-900">{product.name}</h3>
//                   <p className="mt-1 text-lg font-semibold text-gray-900">{product.price}</p>
//                 </div>
//                 <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition">
//                   <button className="bg-white p-2 rounded-full shadow hover:bg-gray-100">
//                     <FiHeart size={18} />
//                   </button>
//                 </div>
//               </div>
//             ))}
//           </div>
//         </section> */}
//       </main>
//     </div>
//   );
// };

// export default HomePage;