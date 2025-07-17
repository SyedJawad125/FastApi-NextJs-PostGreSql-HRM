// 'use client'
// import React, { useEffect, useState, useRef } from 'react';
// import { useRouter } from 'next/navigation';
// import { ToastContainer, toast } from 'react-toastify';
// import 'react-toastify/dist/ReactToastify.css';
// import AxiosInstance from "@/components/AxiosInstance";

// const PublicCategory = () => {
//     const router = useRouter();
//     const [records, setRecords] = useState([]);
//     const [data, setData] = useState([]);
//     const [flag, setFlag] = useState(false);
//     const [categories, setCategories] = useState([]);
//     const [sliderHeight, setSliderHeight] = useState('auto');
//     const productsRef = useRef(null);
//     const resizeObserverRef = useRef(null);

//     // Fetch products and categories
//     useEffect(() => {
//         if (router.query && router.query.name) {
//             toast.success(router.query.name);
//             router.push('/products', undefined, { shallow: true });
//         } else if (flag) {
//             toast.success('Product deleted');
//             setFlag(false);
//         }

//         const fetchData = async () => {
//             try {
//                 // Fetch categories (main content)
//                 const categoriesRes = await AxiosInstance.get('/ecommerce/publiccategory');
//                 if (categoriesRes) {
//                     setRecords(categoriesRes.data.data.data);
//                     setData(categoriesRes.data);
//                 }

//                 // Fetch products (for the slider)
//                 const productsRes = await AxiosInstance.get('/ecommerce/publicproduct');
//                 if (productsRes && productsRes.data) {
//                     setCategories(productsRes.data.data.data);
//                 }
//             } catch (error) {
//                 console.log('Error occurred', error);
//             }
//         };

//         fetchData();
//     }, [flag, router.query?.name]);

//     // Update slider height when records change or window resizes
//     useEffect(() => {
//         const updateSliderHeight = () => {
//             if (productsRef.current) {
//                 const productsHeight = productsRef.current.offsetHeight;
//                 setSliderHeight(`${productsHeight}px`);
//             }
//         };

//         // Initialize ResizeObserver to track content changes
//         if (!resizeObserverRef.current && productsRef.current) {
//             resizeObserverRef.current = new ResizeObserver(updateSliderHeight);
//             resizeObserverRef.current.observe(productsRef.current);
//         }

//         // Initial height calculation
//         updateSliderHeight();

//         // Cleanup
//         return () => {
//             if (resizeObserverRef.current) {
//                 resizeObserverRef.current.disconnect();
//             }
//         };
//     }, [records]);

//     const handleCategoryClick = (categoryId) => {
//         router.push(`/categorywiseproductpage?categoryId=${categoryId}`);
//     };

//     const handleProductClick = (ProductId) => {
//         router.push(`/productdetailpage?ProductId=${ProductId}`);
//     };

//     return (
//         <div className="flex min-h-screen bg-gray-50">
//   {/* Left Side - Products Slider (polished like earlier version) */}
//   <div className="w-[10%] bg-gray-100 shadow-lg relative overflow-hidden ml-2" style={{ height: sliderHeight }}>
//     <div className="absolute top-0 left-0 right-0 animate-scrollUp">
//       {[...categories, ...categories].map((product, index) => (
//         <div
//           key={`${product.id}-${index}`}
//           onClick={() => handleProductClick(product.id)}
//           className="shadow-md cursor-pointer p-2 hover:bg-gray-400 transition duration-300"
//         >
//           <img
//             src={`http://localhost:8000/${product.image}`}
//             className="w-full h-28 object-cover rounded"
//             alt={product.name}
//           />
//         </div>
//       ))}
//     </div>

//     {/* Top and Bottom Gradient Masks */}
//     <div className="absolute top-0 left-0 right-0 h-12 bg-gradient-to-b from-gray-100 to-transparent z-10 pointer-events-none" />
//     <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-gray-100 to-transparent z-10 pointer-events-none" />
//   </div>

//   {/* Right Side - Categories */}
//   <div className="w-[85%] p-8" ref={productsRef}>
//     <h2 className="text-4xl font-serif text-gray-900 font-bold -mb-10 mt-10 text-center tracking-wider">Collections</h2>

//     <br />
//     <br />
//     {data && data.data ? <p>Total: {data.data.count}</p> : <p>Total: 0</p>}
//     <br/>

//     <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-8 gap-2">
//       {records.length > 0 ? (
//         records.map((item) => (
//           <div
//             key={item.id}
//             className="card-5 cursor-pointer"
//             onClick={() => handleCategoryClick(item.id)}
//           >
//             <img
//               src={`http://localhost:8000/${item.image}`}
//               className="card-image5 clickable-image w-full h-40 object-cover transform transition-transform duration-300 hover:scale-105 border border-black"
//               alt={item.name}
//             />
//             <div className="card-body5 p-4">
//               <h5 className="card-title text-black text-sm font-medium -m-6 p-3">{item.name}</h5>
//               <p className="card-text text-black text-xs mt-1 -m-6 p-3">Des: {item.description}</p>
//               <p className="card-text text-black text-xs mt-1 font-semibold -m-6 p-3">Price: {item.price}</p>
//             </div>
//           </div>
//         ))
//       ) : (
//         <p>Loading....</p>
//       )}
//     </div>

//     <div className="h-8"></div>
//   </div>

//   <ToastContainer />

//   {/* Animation Style */}
//   <style jsx>{`
//     @keyframes scrollUp {
//       0% {
//         transform: translateY(0);
//       }
//       100% {
//         transform: translateY(-${categories.length * 120}px);
//       }
//     }
//     .animate-scrollUp {
//       animation: scrollUp ${categories.length * 5}s linear infinite;
//     }
//   `}</style>
// </div>

//     );
// };

// export default PublicCategory;




// 'use client'
// import React, { useEffect, useState, useRef } from 'react';
// import { useRouter } from 'next/navigation';
// import { ToastContainer, toast } from 'react-toastify';
// import 'react-toastify/dist/ReactToastify.css';
// import AxiosInstance from "@/components/AxiosInstance";

// const PublicCategory = () => {
//     const router = useRouter();
//     const [records, setRecords] = useState([]);
//     const [paginationData, setPaginationData] = useState({
//         count: 0,
//         total_pages: 1,
//         current_page: 1,
//         limit: 24,
//         offset: 0,
//         next: false,
//         previous: false
//     });
//     const [loading, setLoading] = useState(false);
//     const [flag, setFlag] = useState(false);
//     const [categories, setCategories] = useState([]);
//     const [sliderHeight, setSliderHeight] = useState('auto');
//     const productsRef = useRef(null);
//     const resizeObserverRef = useRef(null);

//     // Fetch categories with pagination
//     const fetchCategories = async (page = 1, limit = 24, offset = 0) => {
//         setLoading(true);
//         try {
//             const params = new URLSearchParams({
//                 page: page.toString(),
//                 limit: limit.toString(),
//                 offset: offset.toString()
//             });

//             const categoriesRes = await AxiosInstance.get(`/ecommerce/publiccategory?${params}`);
//             if (categoriesRes && categoriesRes.data.data) {
//                 setRecords(categoriesRes.data.data.data);
//                 setPaginationData({
//                     count: categoriesRes.data.data.count,
//                     total_pages: categoriesRes.data.data.total_pages,
//                     current_page: categoriesRes.data.data.current_page,
//                     limit: categoriesRes.data.data.limit,
//                     offset: categoriesRes.data.data.offset,
//                     next: categoriesRes.data.data.next,
//                     previous: categoriesRes.data.data.previous,
//                 });
//             }
//         } catch (error) {
//             console.log('Error occurred', error);
//             toast.error('Failed to load categories');
//         } finally {
//             setLoading(false);
//         }
//     };

//     // Initial data fetch
//     useEffect(() => {
//         if (router.query && router.query.name) {
//             toast.success(router.query.name);
//             router.push('/products', undefined, { shallow: true });
//         } else if (flag) {
//             toast.success('Product deleted');
//             setFlag(false);
//         }

//         const fetchInitialData = async () => {
//             await fetchCategories();
            
//             // Fetch products for the slider
//             try {
//                 const productsRes = await AxiosInstance.get('/ecommerce/publicproduct');
//                 if (productsRes && productsRes.data) {
//                     setCategories(productsRes.data.data.data);
//                 }
//             } catch (error) {
//                 console.log('Error occurred', error);
//             }
//         };

//         fetchInitialData();
//     }, [flag, router.query?.name]);

//     // Handle page change
//     const handlePageChange = (newPage) => {
//         if (newPage > 0 && newPage <= paginationData.total_pages) {
//             fetchCategories(newPage, paginationData.limit, paginationData.offset);
//         }
//     };

//     // Handle limit change
//     const handleLimitChange = (e) => {
//         const newLimit = parseInt(e.target.value);
//         fetchCategories(1, newLimit, 0);
//     };

//     // Update slider height when records change or window resizes
//     useEffect(() => {
//         const updateSliderHeight = () => {
//             if (productsRef.current) {
//                 const productsHeight = productsRef.current.offsetHeight;
//                 setSliderHeight(`${productsHeight}px`);
//             }
//         };

//         if (!resizeObserverRef.current && productsRef.current) {
//             resizeObserverRef.current = new ResizeObserver(updateSliderHeight);
//             resizeObserverRef.current.observe(productsRef.current);
//         }

//         updateSliderHeight();

//         return () => {
//             if (resizeObserverRef.current) {
//                 resizeObserverRef.current.disconnect();
//             }
//         };
//     }, [records]);

//     const handleCategoryClick = (categoryId) => {
//         router.push(`/categorywiseproductpage?categoryId=${categoryId}`);
//     };

//     const handleProductClick = (ProductId) => {
//         router.push(`/productdetailpage?ProductId=${ProductId}`);
//     };

//     return (
//         <div className="flex min-h-screen bg-gray-50">
//             {/* Left Side - Products Slider */}
//             <div className="w-[10%] bg-gray-100 shadow-lg relative overflow-hidden ml-2" style={{ height: sliderHeight }}>
//                 <div className="absolute top-0 left-0 right-0 animate-scrollUp">
//                     {[...categories, ...categories].map((product, index) => (
//                         <div
//                             key={`${product.id}-${index}`}
//                             onClick={() => handleProductClick(product.id)}
//                             className="shadow-md cursor-pointer p-2 hover:bg-gray-400 transition duration-300"
//                         >
//                             <img
//                                 src={`http://localhost:8000/${product.image}`}
//                                 className="w-full h-28 object-cover rounded"
//                                 alt={product.name}
//                             />
//                         </div>
//                     ))}
//                 </div>
//                 <div className="absolute top-0 left-0 right-0 h-12 bg-gradient-to-b from-gray-100 to-transparent z-10 pointer-events-none" />
//                 <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-gray-100 to-transparent z-10 pointer-events-none" />
//             </div>

//             {/* Right Side - Categories */}
//             <div className="w-[85%] p-8" ref={productsRef}>
//                 <h2 className="text-4xl font-serif text-gray-900 font-bold -mb-10 mt-10 text-center tracking-wider">
//                     Collections
//                 </h2>

//                 <br /><br />
//                 <div className="flex justify-between items-center mb-4">
//                     <p className="text-black">Total: {paginationData.count}</p>
//                     <div className="flex items-center gap-2 text-black">
//                         <span>Items per page:</span>
//                         <select 
//                             value={paginationData.limit}
//                             onChange={handleLimitChange}
//                             className="border rounded p-1 text-black"
//                         >
//                             <option value="8">8</option>
//                             <option value="16">16</option>
//                             <option value="24">24</option>
//                             <option value="32">32</option>
//                         </select>
//                     </div>
//                 </div>

//                 {loading ? (
//                     <p>Loading....</p>
//                 ) : (
//                     <>
//                         <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-8 gap-2">
//                             {records.length > 0 ? (
//                                 records.map((item) => (
//                                     <div
//                                         key={item.id}
//                                         className="card-5 cursor-pointer"
//                                         onClick={() => handleCategoryClick(item.id)}
//                                     >
//                                         <img
//                                             src={`http://localhost:8000/${item.image}`}
//                                             className="card-image5 clickable-image w-full h-40 object-cover transform transition-transform duration-300 hover:scale-105 border border-black"
//                                             alt={item.name}
//                                         />
//                                         <div className="card-body5 p-4">
//                                             <h5 className="text-black text-sm font-medium -m-6 p-3">{item.name}</h5>
//                                             <p className="text-black text-xs mt-1 -m-6 p-3">Des: {item.description}</p>
//                                             <p className="text-black text-xs mt-1 font-semibold -m-6 p-3">Price: {item.price}</p>
//                                         </div>
//                                     </div>
//                                 ))
//                             ) : (
//                                 <p>No categories found</p>
//                             )}
//                         </div>

//                         {/* Pagination controls */}
//                         <div className="flex justify-center mt-8 gap-2">
//                             <button
//                                 onClick={() => handlePageChange(paginationData.current_page - 1)}
//                                 disabled={!paginationData.previous || loading}
//                                 className={`px-4 py-2 rounded ${!paginationData.previous ? 'bg-gray-300 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600 text-white'}`}
//                             >
//                                 Previous
//                             </button>
                            
//                             <div className="flex items-center gap-1">
//                                 {Array.from({ length: Math.min(5, paginationData.total_pages) }, (_, i) => {
//                                     let pageNum;
//                                     if (paginationData.total_pages <= 5) {
//                                         pageNum = i + 1;
//                                     } else if (paginationData.current_page <= 3) {
//                                         pageNum = i + 1;
//                                     } else if (paginationData.current_page >= paginationData.total_pages - 2) {
//                                         pageNum = paginationData.total_pages - 4 + i;
//                                     } else {
//                                         pageNum = paginationData.current_page - 2 + i;
//                                     }
                                    
//                                     return (
//                                         <button
//                                             key={pageNum}
//                                             onClick={() => handlePageChange(pageNum)}
//                                             className={`px-3 py-1 rounded ${paginationData.current_page === pageNum ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
//                                         >
//                                             {pageNum}
//                                         </button>
//                                     );
//                                 })}
                                
//                                 {paginationData.total_pages > 5 && paginationData.current_page < paginationData.total_pages - 2 && (
//                                     <>
//                                         <span>...</span>
//                                         <button
//                                             onClick={() => handlePageChange(paginationData.total_pages)}
//                                             className={`px-3 py-1 rounded ${paginationData.current_page === paginationData.total_pages ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
//                                         >
//                                             {paginationData.total_pages}
//                                         </button>
//                                     </>
//                                 )}
//                             </div>
                            
//                             <button
//                                 onClick={() => handlePageChange(paginationData.current_page + 1)}
//                                 disabled={!paginationData.next || loading}
//                                 className={`px-4 py-2 rounded ${!paginationData.next ? 'bg-gray-300 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600 text-white'}`}
//                             >
//                                 Next
//                             </button>
//                         </div>
//                     </>
//                 )}
//             </div>

//             <ToastContainer />

//             <style jsx>{`
//                 @keyframes scrollUp {
//                     0% {
//                         transform: translateY(0);
//                     }
//                     100% {
//                         transform: translateY(-${categories.length * 120}px);
//                     }
//                 }
//                 .animate-scrollUp {
//                     animation: scrollUp ${categories.length * 5}s linear infinite;
//                 }
//             `}</style>
//         </div>
//     );
// };

// export default PublicCategory;




'use client'
import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AxiosInstance from "@/components/AxiosInstance";

const PublicCategory = () => {
    const router = useRouter();
    const [records, setRecords] = useState([]);
    const [paginationData, setPaginationData] = useState({
        count: 0,
        total_pages: 1,
        current_page: 1,
        limit: 24,
        offset: 0,
        next: false,
        previous: false
    });
    const [loading, setLoading] = useState(false);
    const [flag, setFlag] = useState(false);
    const [categories, setCategories] = useState([]);
    const [sliderHeight, setSliderHeight] = useState('auto');
    const productsRef = useRef(null);
    const resizeObserverRef = useRef(null);
    const baseURL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

    // Fetch categories with pagination
    const fetchCategories = async (page = 1, limit = 24, offset = 0) => {
        setLoading(true);
        try {
            const params = new URLSearchParams({
                page: page.toString(),
                limit: limit.toString(),
                offset: offset.toString()
            });

            const categoriesRes = await AxiosInstance.get(`/ecommerce/publiccategory?${params}`);
            if (categoriesRes && categoriesRes.data.data) {
                setRecords(categoriesRes.data.data.data);
                setPaginationData({
                    count: categoriesRes.data.data.count,
                    total_pages: categoriesRes.data.data.total_pages,
                    current_page: categoriesRes.data.data.current_page,
                    limit: categoriesRes.data.data.limit,
                    offset: categoriesRes.data.data.offset,
                    next: categoriesRes.data.data.next,
                    previous: categoriesRes.data.data.previous,
                });
            }
        } catch (error) {
            console.log('Error occurred', error);
            toast.error('Failed to load categories');
        } finally {
            setLoading(false);
        }
    };

    // Initial data fetch
    useEffect(() => {
        if (router.query && router.query.name) {
            toast.success(router.query.name);
            router.push('/products', undefined, { shallow: true });
        } else if (flag) {
            toast.success('Product deleted');
            setFlag(false);
        }

        const fetchInitialData = async () => {
            await fetchCategories();
            
            // Fetch products for the slider
            try {
                const productsRes = await AxiosInstance.get('/ecommerce/publicproduct');
                if (productsRes && productsRes.data) {
                    // Process the products to include proper image URLs
                    const processedProducts = productsRes.data.data.data.map(product => ({
                        ...product,
                        mainImage: product.image_urls?.[0] 
                            ? `${baseURL}${product.image_urls[0].startsWith('/') ? '' : '/'}${product.image_urls[0]}`
                            : '/default-product-image.jpg',
                        remainingImages: product.image_urls?.slice(1).map(u => 
                            `${baseURL}${u.startsWith('/') ? '' : '/'}${u}`
                        ) || []
                    }));
                    setCategories(processedProducts);
                }
            } catch (error) {
                console.log('Error occurred', error);
            }
        };

        fetchInitialData();
    }, [flag, router.query?.name]);

    // Handle page change
    const handlePageChange = (newPage) => {
        if (newPage > 0 && newPage <= paginationData.total_pages) {
            fetchCategories(newPage, paginationData.limit, paginationData.offset);
        }
    };

    // Handle limit change
    const handleLimitChange = (e) => {
        const newLimit = parseInt(e.target.value);
        fetchCategories(1, newLimit, 0);
    };

    // Update slider height when records change or window resizes
    useEffect(() => {
        const updateSliderHeight = () => {
            if (productsRef.current) {
                const productsHeight = productsRef.current.offsetHeight;
                setSliderHeight(`${productsHeight}px`);
            }
        };

        if (!resizeObserverRef.current && productsRef.current) {
            resizeObserverRef.current = new ResizeObserver(updateSliderHeight);
            resizeObserverRef.current.observe(productsRef.current);
        }

        updateSliderHeight();

        return () => {
            if (resizeObserverRef.current) {
                resizeObserverRef.current.disconnect();
            }
        };
    }, [records]);

    const handleCategoryClick = (categoryId) => {
        router.push(`/categorywiseproductpage?categoryId=${categoryId}`);
    };

    const handleProductClick = (product) => {
        const query = new URLSearchParams({
            ProductId: product.id.toString(),
            productData: JSON.stringify(product)
        }).toString();
        router.push(`/productdetailpage?${query}`);
    };

    return (
        <div className="flex min-h-screen bg-gray-50">
            {/* Left Side - Products Slider */}
            <div className="w-[10%] bg-gray-100 shadow-lg relative overflow-hidden ml-2" style={{ height: sliderHeight }}>
                <div className="absolute top-0 left-0 right-0 animate-scrollUp">
                    {[...categories, ...categories].map((product, index) => (
                        <div
                            key={`${product.id}-${index}`}
                            onClick={() => handleProductClick(product)}
                            className="shadow-md cursor-pointer p-2 hover:bg-gray-400 transition duration-300"
                        >
                            <img
                                src={product.mainImage}
                                className="w-full h-28 object-cover rounded"
                                alt={product.name}
                            />
                            <div className="mt-1 text-xs text-center line-clamp-1">
                                {/* {product.name} */}
                            </div>
                        </div>
                    ))}
                </div>
                <div className="absolute top-0 left-0 right-0 h-12 bg-gradient-to-b from-gray-100 to-transparent z-10 pointer-events-none" />
                <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-gray-100 to-transparent z-10 pointer-events-none" />
            </div>

            {/* Right Side - Categories */}
            <div className="w-[85%] p-8" ref={productsRef}>
                <h2 className="text-4xl font-serif text-gray-900 font-bold -mb-10 mt-10 text-center tracking-wider">
                    Collections
                </h2>

                <br /><br />
                <div className="flex justify-between items-center mb-4">
                    <p className="text-black">Total: {paginationData.count}</p>
                    <div className="flex items-center gap-2 text-black">
                        <span>Items per page:</span>
                        <select 
                            value={paginationData.limit}
                            onChange={handleLimitChange}
                            className="border rounded p-1 text-black"
                        >
                            <option value="8">8</option>
                            <option value="16">16</option>
                            <option value="24">24</option>
                            <option value="32">32</option>
                        </select>
                    </div>
                </div>

                {loading ? (
                    <p>Loading....</p>
                ) : (
                    <>
                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-8 gap-2">
                            {records.length > 0 ? (
                                records.map((item) => (
                                    <div
                                        key={item.id}
                                        className="card-5 cursor-pointer group relative mb-2"
                                        onClick={() => handleCategoryClick(item.id)}
                                    >
                                        <img
                                            src={`${baseURL}${item.image.startsWith('/') ? '' : '/'}${item.image}`}
                                            className="card-image5 clickable-image w-full h-40 object-cover transform transition-transform duration-300 hover:scale-105 border border-black"
                                            alt={item.name}
                                        />
                                        <div className="card-body5 p-4">
                                            <h5 className="text-black text-sm font-medium -m-6 p-3">{item.name}</h5>
                                            <p className="text-black text-xs mt-1 -m-6 p-3 line-clamp-2">Des: {item.description}</p>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <p>No categories found</p>
                            )}
                        </div>

                        {/* Pagination controls */}
                        <div className="flex justify-center mt-8 gap-2">
                            <button
                                onClick={() => handlePageChange(paginationData.current_page - 1)}
                                disabled={!paginationData.previous || loading}
                                className={`px-4 py-2 rounded ${!paginationData.previous ? 'bg-gray-300 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600 text-white'}`}
                            >
                                Previous
                            </button>
                            
                            <div className="flex items-center gap-1">
                                {Array.from({ length: Math.min(5, paginationData.total_pages) }, (_, i) => {
                                    let pageNum;
                                    if (paginationData.total_pages <= 5) {
                                        pageNum = i + 1;
                                    } else if (paginationData.current_page <= 3) {
                                        pageNum = i + 1;
                                    } else if (paginationData.current_page >= paginationData.total_pages - 2) {
                                        pageNum = paginationData.total_pages - 4 + i;
                                    } else {
                                        pageNum = paginationData.current_page - 2 + i;
                                    }
                                    
                                    return (
                                        <button
                                            key={pageNum}
                                            onClick={() => handlePageChange(pageNum)}
                                            className={`px-3 py-1 rounded ${paginationData.current_page === pageNum ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
                                        >
                                            {pageNum}
                                        </button>
                                    );
                                })}
                                
                                {paginationData.total_pages > 5 && paginationData.current_page < paginationData.total_pages - 2 && (
                                    <>
                                        <span>...</span>
                                        <button
                                            onClick={() => handlePageChange(paginationData.total_pages)}
                                            className={`px-3 py-1 rounded ${paginationData.current_page === paginationData.total_pages ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
                                        >
                                            {paginationData.total_pages}
                                        </button>
                                    </>
                                )}
                            </div>
                            
                            <button
                                onClick={() => handlePageChange(paginationData.current_page + 1)}
                                disabled={!paginationData.next || loading}
                                className={`px-4 py-2 rounded ${!paginationData.next ? 'bg-gray-300 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600 text-white'}`}
                            >
                                Next
                            </button>
                        </div>
                    </>
                )}
            </div>

            <ToastContainer />

            <style jsx>{`
                @keyframes scrollUp {
                    0% {
                        transform: translateY(0);
                    }
                    100% {
                        transform: translateY(-${categories.length * 120}px);
                    }
                }
                .animate-scrollUp {
                    animation: scrollUp ${categories.length * 5}s linear infinite;
                }
            `}</style>
        </div>
    );
};

export default PublicCategory;