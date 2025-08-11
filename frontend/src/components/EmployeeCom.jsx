// 'use client';
// import React, { useEffect, useState, useContext, useRef } from 'react';
// import { ToastContainer, toast } from 'react-toastify';
// import 'react-toastify/dist/ReactToastify.css';
// import AxiosInstance from "@/components/AxiosInstance";
// import { useRouter } from 'next/navigation';
// import { AuthContext } from '@/components/AuthContext';

// const EmployeeCom = () => {
//   const router = useRouter();
//   const { permissions = {
//     create_employee: false,
//     read_employee: false,
//     update_employee: false,
//     delete_employee: false
//   } } = useContext(AuthContext);
  
//   const [records, setRecords] = useState([]);
//   const [filteredRecords, setFilteredRecords] = useState([]);
//   const [searchTerm, setSearchTerm] = useState('');
//   const [pagination, setPagination] = useState({
//     currentPage: 1,
//     limit: 12,
//     offset: 0,
//     totalPages: 1,
//     count: 0,
//     next: false,
//     previous: false
//   });
//   const [isLoading, setIsLoading] = useState(true);
//   const [refreshKey, setRefreshKey] = useState(0);

//   // Fetch employees with pagination
//   useEffect(() => {
//     const fetchEmployees = async () => {
//       if (!permissions.read_employee) {
//         setIsLoading(false);
//         return;
//       }

//       setIsLoading(true);
//       try {
//         const { currentPage, limit, offset } = pagination;
//         const res = await AxiosInstance.get(
//           `/employees/employee?page=${currentPage}&limit=${limit}&offset=${offset}`
//         );
        
//         // Fixed: Access the correct response structure
//         const responseData = res?.data?.result;
//         const dataArr = responseData?.data || [];
        
//         setRecords(dataArr);
//         setFilteredRecords(dataArr);
        
//         // Calculate total pages from count and limit
//         const totalPages = Math.ceil((responseData?.count || 0) / limit);
        
//         setPagination(prev => ({
//           ...prev,
//           count: responseData?.count || 0,
//           totalPages,
//           next: currentPage < totalPages,
//           previous: currentPage > 1
//         }));
//       } catch (e) {
//         console.error('Error fetching employees:', e);
//         if (e.response?.status === 403) {
//           toast.error('You do not have permission to view employees');
//         } else {
//           toast.error('Failed to load employees', { theme: 'dark', autoClose: 2000 });
//         }
//       } finally {
//         setIsLoading(false);
//       }
//     };

//     fetchEmployees();
//   }, [refreshKey, pagination.currentPage, pagination.limit, pagination.offset, permissions.read_employee]);

//   // Handle pagination change
//   const handlePageChange = (newPage) => {
//     if (newPage >= 1 && newPage <= pagination.totalPages) {
//       setPagination(prev => ({ 
//         ...prev, 
//         currentPage: newPage,
//         offset: (newPage - 1) * prev.limit
//       }));
//     }
//   };

//   // Handle limit change
//   const handleLimitChange = (e) => {
//     const newLimit = parseInt(e.target.value);
//     setPagination(prev => ({ 
//       ...prev, 
//       limit: newLimit,
//       currentPage: 1,
//       offset: 0
//     }));
//   };

//   // Handle offset change
//   const handleOffsetChange = (e) => {
//     const newOffset = Math.max(0, parseInt(e.target.value)) || 0;
//     const newPage = Math.floor(newOffset / pagination.limit) + 1;
//     setPagination(prev => ({ 
//       ...prev, 
//       offset: newOffset,
//       currentPage: newPage
//     }));
//   };

//   const deleteRecord = async (id) => {
//     if (!permissions.delete_employee) {
//       toast.error('You do not have permission to delete employees');
//       return;
//     }
    
//     if (!window.confirm('Are you sure you want to delete this employee?')) return;
    
//     try {
//       await AxiosInstance.delete(`/employees/employee?id=${id}`);
//       setRefreshKey(k => k + 1);
//       toast.success('Employee removed successfully', { theme: 'dark', autoClose: 2000 });
//     } catch (error) {
//       console.error('Error deleting employee:', error);
//       toast.error('Error deleting employee', { theme: 'dark', autoClose: 2000 });
//     }
//   };

//   const updateRecord = (empid) => {
//     if (!permissions.update_employee) {
//       toast.error('You do not have permission to update employees');
//       return;
//     }
//     router.push(`/updateemployeepage?empid=${empid}`);
//   };

//   const DetailRecord = (employeeId) => {
//     if (!permissions.read_employee) {
//       toast.error('You do not have permission to view employee details');
//       return;
//     }
//     router.push(`/epmloyeesdetail?EpmloyeeId=${employeeId}`);
//   };

//   const handleSearch = (e) => {
//     const value = e.target.value.toLowerCase();
//     setSearchTerm(value);
    
//     const filtered = records.filter(r => 
//       r.id.toString() === value ||
//       r.name?.toLowerCase().includes(value) ||
//       r.job_title?.toLowerCase().includes(value) ||
//       r.email?.toLowerCase().includes(value)
//     );
    
//     setFilteredRecords(filtered);
//     setPagination(prev => ({ ...prev, currentPage: 1 }));
//   };

//   // Extract first and last name from full name
//   const getNameParts = (fullName) => {
//     if (!fullName) return { firstName: '', lastName: '' };
//     const parts = fullName.split(' ');
//     return {
//       firstName: parts[0] || '',
//       lastName: parts.slice(1).join(' ') || ''
//     };
//   };

//   // Return early if no read permission
//   if (!permissions.read_employee) {
//     return (
//       <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 flex items-center justify-center">
//         <div className="text-center p-8 max-w-md">
//           <h2 className="text-2xl text-amber-400 mb-4">Access Denied</h2>
//           <p className="text-gray-300 mb-6">
//             You don't have permission to view employees. Please contact your administrator.
//           </p>
//           <button 
//             onClick={() => router.push('/')}
//             className="px-6 py-2 bg-amber-600 rounded-full hover:bg-amber-700 text-white transition-colors"
//           >
//             Return to Dashboard
//           </button>
//         </div>
//         <ToastContainer position="top-right" autoClose={2000} />
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 py-12 px-4">
//       <ToastContainer position="top-right" autoClose={2000} />
      
//       <div className="max-w-7xl mx-auto">
//         {/* Header Section */}
//         <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12">
//           <div>
//             <h1 className="text-4xl font-light text-white">EMPLOYEE RECORDS</h1>
//             <div className="w-20 h-1 bg-gradient-to-r from-amber-400 to-amber-600 mt-1"></div>
//           </div>
          
//           {permissions.create_employee && (
//             <button 
//               onClick={() => router.push('/addemployeepage')}
//               className="px-6 py-3 border border-amber-500 text-amber-500 rounded-full hover:bg-amber-500 hover:text-black transform hover:scale-105 transition-transform mt-4 md:mt-0"
//             >
//               Add Employee
//             </button>
//           )}
//         </div>

//         {/* Search and Stats Section */}
//         <div className="flex flex-col md:flex-row justify-between items-start md:items-center p-4 bg-gray-800/50 rounded-xl mb-8 gap-4">
//           <div className="text-amber-400">
//             Showing {filteredRecords.length} of {pagination.count} items
//             {pagination.offset > 0 && ` (offset: ${pagination.offset})`}
//           </div>
          
//           <div className="flex flex-col md:flex-row gap-4 w-full md:w-2/3">
//             <div className="relative w-full">
//               <span className="absolute left-3 top-3 text-gray-400">
//                 🔍
//               </span>
//               <input 
//                 type="text" 
//                 value={searchTerm} 
//                 onChange={handleSearch}
//                 placeholder="Search by name, ID, job title or email..."
//                 className="w-full pl-10 py-3 bg-gray-700 rounded-full text-white focus:ring-amber-500 focus:outline-none"
//               />
//             </div>
            
//             <div className="flex gap-2 items-center">
//               <select 
//                 value={pagination.limit}
//                 onChange={handleLimitChange}
//                 className="bg-gray-700 text-white rounded-full px-3 py-2 focus:outline-none focus:ring-amber-500"
//               >
//                 <option value="12">12 per page</option>
//                 <option value="24">24 per page</option>
//                 <option value="36">36 per page</option>
//                 <option value="48">48 per page</option>
//               </select>
              
//               <input
//                 type="number"
//                 value={pagination.offset}
//                 onChange={handleOffsetChange}
//                 min="0"
//                 max={Math.max(0, pagination.count - 1)}
//                 placeholder="Offset"
//                 className="bg-gray-700 text-white rounded-full px-3 py-2 w-20 focus:outline-none focus:ring-amber-500"
//               />
//             </div>
//           </div>
//         </div>

//         {/* Employee Table */}
//         <div className="bg-gray-800 rounded-xl overflow-hidden shadow-2xl">
//           {/* Table Header */}
//           <div className="grid grid-cols-12 bg-gray-900 p-4 text-gray-300 font-semibold uppercase text-sm tracking-wider">
//             <div className="col-span-1">S.No</div>
//             <div className="col-span-2">ID</div>
//             <div className="col-span-3">Name</div>
//             <div className="col-span-2">Job Title</div>
//             <div className="col-span-2">Salary</div>
//             <div className="col-span-2 text-right">Actions</div>
//           </div>

//           {/* Table Body */}
//           {isLoading ? (
//             <div className="p-8 text-center text-gray-400">
//               <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-500 mx-auto mb-4"></div>
//               <p className="text-xl">Loading employees...</p>
//             </div>
//           ) : filteredRecords.length > 0 ? (
//             <ul className="divide-y divide-gray-700">
//               {filteredRecords.map((item, index) => {
//                 const { firstName, lastName } = getNameParts(item.name);
//                 const displayIndex = pagination.offset + index + 1;
                
//                 return (
//                   <li key={item.id} className="hover:bg-gray-750 transition-colors duration-200">
//                     <div className="grid grid-cols-12 items-center p-4">
//                       <div className="col-span-1 text-gray-300">{displayIndex}</div>
//                       <div className="col-span-2 text-white font-medium">{item.id}</div>
//                       <div className="col-span-3 text-white">
//                         <div className="flex items-center">
//                           <div className="flex-shrink-0 h-10 w-10 bg-amber-600 rounded-full flex items-center justify-center text-white font-bold mr-3">
//                             {firstName?.charAt(0)}{lastName?.charAt(0)}
//                           </div>
//                           <div>
//                             <p className="font-medium">{item.name}</p>
//                             <p className="text-gray-400 text-sm">{item.email}</p>
//                           </div>
//                         </div>
//                       </div>
//                       <div className="col-span-2 text-gray-300">{item.job_title}</div>
//                       <div className="col-span-2">
//                         <span className="bg-gray-700 text-green-400 px-3 py-1 rounded-full text-xs font-medium">
//                           ${item.salary?.toLocaleString() || 'N/A'}
//                         </span>
//                       </div>
//                       <div className="col-span-2 flex justify-end space-x-2">
//                         <button
//                           onClick={() => DetailRecord(item.id)}
//                           className="p-2 rounded-full bg-gray-700 text-blue-400 hover:bg-gray-600 hover:text-blue-300 transition-colors"
//                           title="View Details"
//                         >
//                           <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
//                             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
//                           </svg>
//                         </button>
                        
//                         {permissions.update_employee && (
//                           <button
//                             onClick={() => updateRecord(item.id)}
//                             className="p-2 rounded-full bg-gray-700 text-green-400 hover:bg-gray-600 hover:text-green-300 transition-colors"
//                             title="Edit"
//                           >
//                             <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
//                             </svg>
//                           </button>
//                         )}
                        
//                         {permissions.delete_employee && (
//                           <button
//                             onClick={() => deleteRecord(item.id)}
//                             className="p-2 rounded-full bg-gray-700 text-red-400 hover:bg-gray-600 hover:text-red-300 transition-colors"
//                             title="Delete"
//                           >
//                             <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
//                             </svg>
//                           </button>
//                         )}
//                       </div>
//                     </div>
//                   </li>
//                 );
//               })}
//             </ul>
//           ) : (
//             <div className="p-8 text-center text-gray-400">
//               <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto mb-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
//               </svg>
//               <p className="text-xl">No employees found</p>
//               <p className="mt-1">Try adjusting your search or add a new employee</p>
//             </div>
//           )}

//           {/* Enhanced Pagination */}
//           {pagination.totalPages > 1 && (
//             <div className="flex flex-col md:flex-row justify-between items-center mt-4 p-4 bg-gray-900 gap-4">
//               <div className="text-gray-400 text-sm">
//                 Page {pagination.currentPage} of {pagination.totalPages} • {pagination.count} total items
//               </div>
              
//               <div className="flex items-center gap-2">
//                 <button 
//                   onClick={() => handlePageChange(1)}
//                   disabled={pagination.currentPage === 1}
//                   className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 disabled:opacity-50 transition-colors text-white"
//                   aria-label="First page"
//                 >
//                   <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
//                     <path fillRule="evenodd" d="M15.707 15.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 010 1.414zm-6 0a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 1.414L5.414 10l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
//                   </svg>
//                 </button>
                
//                 <button 
//                   onClick={() => handlePageChange(pagination.currentPage - 1)}
//                   disabled={!pagination.previous}
//                   className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 disabled:opacity-50 transition-colors text-white"
//                   aria-label="Previous page"
//                 >
//                   <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
//                     <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
//                   </svg>
//                 </button>
                
//                 <div className="flex items-center gap-1">
//                   {Array.from({ length: Math.min(5, pagination.totalPages) }, (_, i) => {
//                     let pageNum;
//                     if (pagination.totalPages <= 5) {
//                       pageNum = i + 1;
//                     } else if (pagination.currentPage <= 3) {
//                       pageNum = i + 1;
//                     } else if (pagination.currentPage >= pagination.totalPages - 2) {
//                       pageNum = pagination.totalPages - 4 + i;
//                     } else {
//                       pageNum = pagination.currentPage - 2 + i;
//                     }
                    
//                     return (
//                       <button 
//                         key={pageNum}
//                         onClick={() => handlePageChange(pageNum)}
//                         className={`w-8 h-8 rounded-full text-sm transition-colors ${
//                           pagination.currentPage === pageNum
//                             ? 'bg-amber-600 text-white'
//                             : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
//                         }`}
//                         aria-label={`Page ${pageNum}`}
//                       >
//                         {pageNum}
//                       </button>
//                     );
//                   })}
//                 </div>
                
//                 <button 
//                   onClick={() => handlePageChange(pagination.currentPage + 1)}
//                   disabled={!pagination.next}
//                   className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 disabled:opacity-50 transition-colors text-white"
//                   aria-label="Next page"
//                 >
//                   <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
//                     <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
//                   </svg>
//                 </button>
                
//                 <button 
//                   onClick={() => handlePageChange(pagination.totalPages)}
//                   disabled={pagination.currentPage === pagination.totalPages}
//                   className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 disabled:opacity-50 transition-colors text-white"
//                   aria-label="Last page"
//                 >
//                   <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
//                     <path fillRule="evenodd" d="M10.293 15.707a1 1 0 010-1.414L14.586 10l-4.293-4.293a1 1 0 111.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clipRule="evenodd" />
//                     <path fillRule="evenodd" d="M4.293 15.707a1 1 0 010-1.414L8.586 10 4.293 5.707a1 1 0 011.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clipRule="evenodd" />
//                   </svg>
//                 </button>
//               </div>
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default EmployeeCom;




'use client';
import React, { useEffect, useState, useContext, useRef } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AxiosInstance from "@/components/AxiosInstance";
import { useRouter } from 'next/navigation';
import { AuthContext } from '@/components/AuthContext';

const EmployeeCom = () => {
  const router = useRouter();
  const { permissions = {
    create_employee: false,
    read_employee: false,
    update_employee: false,
    delete_employee: false
  } } = useContext(AuthContext);
  
  const [records, setRecords] = useState([]);
  const [filteredRecords, setFilteredRecords] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [pagination, setPagination] = useState({
    currentPage: 1,
    limit: 12,
    offset: 0,
    totalPages: 1,
    count: 0,
    next: false,
    previous: false
  });
  const [isLoading, setIsLoading] = useState(true);
  const [refreshKey, setRefreshKey] = useState(0);

  // Fetch employees with pagination
  useEffect(() => {
    const fetchEmployees = async () => {
      if (!permissions.read_employee) {
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      try {
        const { currentPage, limit, offset } = pagination;
        const res = await AxiosInstance.get(
          `/employees/employee?page=${currentPage}&limit=${limit}&offset=${offset}`
        );
        
        const responseData = res?.data?.result;
        const dataArr = responseData?.data || [];
        const totalCount = responseData?.count || 0;
        
        setRecords(dataArr);
        setFilteredRecords(dataArr);
        setPagination(prev => ({
          ...prev,
          count: totalCount,
          totalPages: Math.ceil(totalCount / limit),
          next: currentPage < Math.ceil(totalCount / limit),
          previous: currentPage > 1
        }));
      } catch (e) {
        console.error('Error fetching employees:', e);
        if (e.response?.status === 403) {
          toast.error('You do not have permission to view employees');
        } else {
          toast.error('Failed to load employees', { theme: 'dark', autoClose: 2000 });
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchEmployees();
  }, [refreshKey, pagination.currentPage, pagination.limit, pagination.offset, permissions.read_employee]);

  // Handle pagination change
  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.totalPages) {
      setPagination(prev => ({ ...prev, currentPage: newPage }));
    }
  };

  // Handle limit change
  const handleLimitChange = (e) => {
    const newLimit = parseInt(e.target.value);
    setPagination(prev => ({ 
      ...prev, 
      limit: newLimit,
      currentPage: 1,
      offset: 0
    }));
  };

  // Handle offset change
  const handleOffsetChange = (e) => {
    const newOffset = Math.max(0, parseInt(e.target.value)) || 0;
    setPagination(prev => ({ 
      ...prev, 
      offset: newOffset,
      currentPage: 1
    }));
  };

  const deleteRecord = async (id) => {
    if (!permissions.delete_employee) {
      toast.error('You do not have permission to delete employees');
      return;
    }
    
    if (!window.confirm('Are you sure you want to delete this employee?')) return;
    
    try {
      await AxiosInstance.delete(`/employees/employee/${id}`);
      setRefreshKey(k => k + 1);
      toast.success('Employee removed successfully', { theme: 'dark', autoClose: 2000 });
    } catch (error) {
      console.error('Error deleting employee:', error);
      toast.error('Error deleting employee', { theme: 'dark', autoClose: 2000 });
    }
  };

  const updateRecord = (empid) => {
    if (!permissions.update_employee) {
      toast.error('You do not have permission to update employees');
      return;
    }
    router.push(`/employees/update/${empid}`);
  };

  const DetailRecord = (employeeId) => {
    if (!permissions.read_employee) {
      toast.error('You do not have permission to view employee details');
      return;
    }
    router.push(`/employees/detail/${employeeId}`);
  };

  const handleSearch = (e) => {
    const value = e.target.value.toLowerCase();
    setSearchTerm(value);
    
    const filtered = records.filter(r => 
      r.id.toString() === value ||
      r.name?.toLowerCase().includes(value) ||
      r.job_title?.toLowerCase().includes(value) ||
      (r.department?.name?.toLowerCase().includes(value) || '')
    );
    
    setFilteredRecords(filtered);
    setPagination(prev => ({ ...prev, currentPage: 1 }));
  };

  // Return early if no read permission
  if (!permissions.read_employee) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 flex items-center justify-center">
        <div className="text-center p-8 max-w-md">
          <h2 className="text-2xl text-amber-400 mb-4">Access Denied</h2>
          <p className="text-gray-300 mb-6">
            You don't have permission to view employees. Please contact your administrator.
          </p>
          <button 
            onClick={() => router.push('/')}
            className="px-6 py-2 bg-amber-600 rounded-full hover:bg-amber-700 text-white transition-colors"
          >
            Return to Dashboard
          </button>
        </div>
        <ToastContainer position="top-right" autoClose={2000} />
      </div>
    );
  }

  return (
  <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 py-12 px-4">
    <ToastContainer position="top-right" autoClose={2000} />

    <div className="max-w-7xl mx-auto">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12">
        <div>
          <h1 className="text-4xl font-light text-white">EMPLOYEE RECORDS</h1>
          <div className="w-20 h-1 bg-gradient-to-r from-amber-400 to-amber-600 mt-1"></div>
        </div>

        {permissions.create_employee && (
          <button
            onClick={() => router.push("/employees/add")}
            className="px-6 py-3 border border-amber-500 text-amber-500 rounded-full hover:bg-amber-500 hover:text-black transform hover:scale-105 transition-transform mt-4 md:mt-0"
          >
            Add Employee
          </button>
        )}
      </div>

      {/* Search & Stats Section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center p-4 bg-gray-800/50 backdrop-blur-lg rounded-xl mb-8 gap-4 shadow-md">
        <div className="text-amber-400">
          Showing {filteredRecords.length} of {pagination.count} items
          {pagination.offset > 0 && ` (offset: ${pagination.offset})`}
        </div>

        <div className="flex flex-col md:flex-row gap-4 w-full md:w-2/3">
          <div className="relative w-full">
            <span className="absolute left-3 top-3 text-gray-400">🔍</span>
            <input
              type="text"
              value={searchTerm}
              onChange={handleSearch}
              placeholder="Search by name, ID, job title or department..."
              className="w-full pl-10 py-3 bg-gray-700/70 rounded-full text-white focus:ring-amber-500 focus:outline-none"
            />
          </div>

          <div className="flex gap-2 items-center">
            <select
              value={pagination.limit}
              onChange={handleLimitChange}
              className="bg-gray-700 text-white rounded-full px-3 py-2 focus:outline-none focus:ring-amber-500"
            >
              <option value="12">12 per page</option>
              <option value="24">24 per page</option>
              <option value="36">36 per page</option>
              <option value="48">48 per page</option>
            </select>

            <input
              type="number"
              value={pagination.offset}
              onChange={handleOffsetChange}
              min="0"
              max={pagination.count}
              placeholder="Offset"
              className="bg-gray-700 text-white rounded-full px-3 py-2 w-20 focus:outline-none focus:ring-amber-500"
            />
          </div>
        </div>
      </div>

      {/* Employee Table */}
      <div className="bg-gray-800/60 backdrop-blur-lg rounded-xl overflow-hidden shadow-2xl border border-gray-700">
        {/* Table Header */}
        <div className="grid grid-cols-12 bg-gray-900/80 p-4 text-gray-300 font-semibold uppercase text-sm tracking-wider border-b border-gray-700">
          <div className="col-span-1">S.No</div>
          <div className="col-span-2">ID</div>
          <div className="col-span-3">Name</div>
          <div className="col-span-2">Job Title</div>
          <div className="col-span-2">Department</div>
          <div className="col-span-2 text-right">Actions</div>
        </div>

        {/* Table Body */}
        {isLoading ? (
          <div className="p-8 text-center text-gray-400">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-500 mx-auto mb-4"></div>
            <p className="text-xl">Loading employees...</p>
          </div>
        ) : filteredRecords.length > 0 ? (
          <ul className="divide-y divide-gray-700">
            {filteredRecords.map((item, index) => (
              <li
                key={item.id}
                className="group transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg"
              >
                <div className="grid grid-cols-12 items-center p-4 bg-gray-800/60 backdrop-blur-md rounded-xl hover:bg-gray-800/80 transition-colors duration-300 border border-gray-700 hover:border-amber-500/50">
                  {/* Serial */}
                  <div className="col-span-1 text-gray-400 font-light">
                    {(pagination.currentPage - 1) * pagination.limit +
                      index +
                      1}
                  </div>

                  {/* ID */}
                  <div className="col-span-2 text-white font-semibold tracking-wide">
                    {item.id}
                  </div>

                  {/* Name + Avatar */}
                  <div className="col-span-3 flex items-center">
                    <div className="h-12 w-12 rounded-full bg-gradient-to-tr from-amber-500 to-amber-700 flex items-center justify-center text-white font-bold shadow-md ring-2 ring-amber-500/40 mr-4">
                      {item.name?.split(" ").map((n) => n.charAt(0)).join("")}
                    </div>
                    <div>
                      <p className="font-medium text-white">{item.name}</p>
                      <p className="text-gray-400 text-xs">{item.email}</p>
                    </div>
                  </div>

                  {/* Job Title */}
                  <div className="col-span-2 text-gray-300">
                    {item.job_title}
                  </div>

                  {/* Department */}
                  <div className="col-span-2">
                    <span className="px-4 py-1 rounded-full text-xs font-medium bg-gradient-to-r from-gray-700 to-gray-600 text-gray-200 shadow-sm">
                      {item.department_id}
                    </span>
                  </div>

                  {/* Actions */}
                  <div className="col-span-2 flex justify-end space-x-2">
                    {/* View */}
                    <button
                      onClick={() => DetailRecord(item.id)}
                      className="p-2 rounded-full bg-gradient-to-tr from-blue-500 to-blue-600 text-white shadow-md hover:shadow-blue-500/40 hover:scale-105 transition"
                      title="View Details"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-4 w-4"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                        />
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                        />
                      </svg>
                    </button>

                    {/* Edit */}
                    {permissions.update_employee && (
                      <button
                        onClick={() => updateRecord(item.id)}
                        className="p-2 rounded-full bg-gradient-to-tr from-green-500 to-green-600 text-white shadow-md hover:shadow-green-500/40 hover:scale-105 transition"
                        title="Edit"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          className="h-4 w-4"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                          />
                        </svg>
                      </button>
                    )}

                    {/* Delete */}
                    {permissions.delete_employee && (
                      <button
                        onClick={() => deleteRecord(item.id)}
                        className="p-2 rounded-full bg-gradient-to-tr from-red-500 to-red-600 text-white shadow-md hover:shadow-red-500/40 hover:scale-105 transition"
                        title="Delete"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          className="h-4 w-4"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                          />
                        </svg>
                      </button>
                    )}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="p-8 text-center text-gray-400">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-12 w-12 mx-auto mb-4 text-gray-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p className="text-xl">No employees found</p>
            <p className="mt-1">
              Try adjusting your search or add a new employee
            </p>
          </div>
        )}

        {/* Pagination */}
        {pagination.totalPages > 1 && (
          <div className="flex flex-col md:flex-row justify-between items-center mt-4 p-4 bg-gray-900/80 gap-4">
            <div className="text-gray-400 text-sm">
              Page {pagination.currentPage} of {pagination.totalPages} •{" "}
              {pagination.count} total items
            </div>

            <div className="flex items-center gap-2">
              {/* First Page */}
              <button
                onClick={() => handlePageChange(1)}
                disabled={pagination.currentPage === 1}
                className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 disabled:opacity-50 transition-colors"
              >
                ⏮
              </button>

              {/* Prev */}
              <button
                onClick={() => handlePageChange(pagination.currentPage - 1)}
                disabled={!pagination.previous}
                className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 disabled:opacity-50 transition-colors"
              >
                ◀
              </button>

              {/* Page Numbers */}
              <div className="flex items-center gap-1">
                {Array.from(
                  { length: Math.min(5, pagination.totalPages) },
                  (_, i) => {
                    let pageNum;
                    if (pagination.totalPages <= 5) {
                      pageNum = i + 1;
                    } else if (pagination.currentPage <= 3) {
                      pageNum = i + 1;
                    } else if (
                      pagination.currentPage >=
                      pagination.totalPages - 2
                    ) {
                      pageNum = pagination.totalPages - 4 + i;
                    } else {
                      pageNum = pagination.currentPage - 2 + i;
                    }

                    return (
                      <button
                        key={pageNum}
                        onClick={() => handlePageChange(pageNum)}
                        className={`w-8 h-8 rounded-full text-sm transition-colors ${
                          pagination.currentPage === pageNum
                            ? "bg-amber-600 text-white"
                            : "bg-gray-700 hover:bg-gray-600 text-gray-300"
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  }
                )}
              </div>

              {/* Next */}
              <button
                onClick={() => handlePageChange(pagination.currentPage + 1)}
                disabled={!pagination.next}
                className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 disabled:opacity-50 transition-colors"
              >
                ▶
              </button>

              {/* Last */}
              <button
                onClick={() => handlePageChange(pagination.totalPages)}
                disabled={pagination.currentPage === pagination.totalPages}
                className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 disabled:opacity-50 transition-colors"
              >
                ⏭
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  </div>

  );
};

export default EmployeeCom;