// import React, { useEffect, useState, useContext } from 'react';
// import AxiosInstance from "@/components/AxiosInstance";
// import { useRouter } from 'next/navigation';
// import { toast } from 'react-hot-toast';
// import { Toaster } from 'react-hot-toast';
// import { AuthContext } from '@/components/AuthContext';

// const AuditLogCom = () => {
//   const router = useRouter();
//   const { permissions = {} } = useContext(AuthContext);
//   const [auditLogsList, setAuditLogsList] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [filters, setFilters] = useState({
//     user_id: '',
//     action: '',
//     table_name: '',
//     start_date: '',
//     end_date: ''
//   });
//   const [pagination, setPagination] = useState({
//     page: 1,
//     limit: 10,
//     total: 0,
//     totalPages: 1
//   });

//   const fetchAuditLogs = async (page = 1, limit = pagination.limit) => {
//     setLoading(true);
//     try {
//       const params = {
//         page,
//         limit,
//         ...Object.fromEntries(
//           Object.entries(filters).filter(([_, v]) => v !== '')
//         )
//       };

//       const response = await AxiosInstance.get('/audit-logs', { params });
      
//       if (response.data.status === 'SUCCESSFUL') {
//         setAuditLogsList(response.data.result.data);
//         setPagination(prev => ({
//           ...prev,
//           page,
//           limit,
//           total: response.data.result.count,
//           totalPages: Math.ceil(response.data.result.count / limit)
//         }));
//       }
//     } catch (error) {
//       console.error(
//         "Audit log fetch error:",
//         error.response?.status,
//         error.response?.data
//       );
//       toast.error('Error fetching audit logs');
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     fetchAuditLogs(pagination.page);
//   }, [pagination.page]);

//   // Add this useEffect to refetch when limit changes
//   useEffect(() => {
//     if (pagination.page === 1) {
//       fetchAuditLogs(1, pagination.limit);
//     } else {
//       setPagination(prev => ({ ...prev, page: 1 }));
//     }
//   }, [pagination.limit]);

//   const handlePageChange = (newPage) => {
//     if (newPage >= 1 && newPage <= pagination.totalPages) {
//       setPagination(prev => ({ ...prev, page: newPage }));
//     }
//   };

//   const handleLimitChange = (newLimit) => {
//     setPagination(prev => ({ ...prev, limit: Number(newLimit) }));
//   };

//   const handleFilterChange = (field, value) => {
//     setFilters(prev => ({ ...prev, [field]: value }));
//   };

//   const applyFilters = () => {
//     setPagination(prev => ({ ...prev, page: 1 }));
//     fetchAuditLogs(1);
//   };

//   const clearFilters = () => {
//     setFilters({
//       user_id: '',
//       action: '',
//       table_name: '',
//       start_date: '',
//       end_date: ''
//     });
//     setPagination(prev => ({ ...prev, page: 1 }));
//     fetchAuditLogs(1);
//   };

//   const formatDateTime = (dateString) => {
//     if (!dateString) return 'N/A';
//     const date = new Date(dateString);
//     return date.toLocaleString('en-US', {
//       year: 'numeric',
//       month: 'short',
//       day: '2-digit',
//       hour: '2-digit',
//       minute: '2-digit',
//       second: '2-digit'
//     });
//   };

//   const getActionColor = (action) => {
//     const colors = {
//       'CREATE': 'from-green-500/20 to-emerald-500/20 text-green-300 border-green-500/30',
//       'UPDATE': 'from-blue-500/20 to-indigo-500/20 text-blue-300 border-blue-500/30',
//       'DELETE': 'from-red-500/20 to-rose-500/20 text-red-300 border-red-500/30',
//       'LOGIN': 'from-amber-500/20 to-yellow-500/20 text-amber-300 border-amber-500/30',
//       'LOGOUT': 'from-gray-500/20 to-slate-500/20 text-gray-300 border-gray-500/30'
//     };
//     return colors[action?.toUpperCase()] || 'from-slate-500/20 to-gray-500/20 text-slate-300 border-slate-500/30';
//   };

//   // Check for read permissions
//   if (!permissions.read_auditlog) {
//     return (
//       <div className="min-h-screen bg-gray-900 flex items-center justify-center p-6">
//         <div className="text-center p-8 max-w-md">
//           <h2 className="text-2xl text-amber-400 mb-4">Access Denied</h2>
//           <p className="text-gray-300 mb-6">
//             You don't have permission to view Audit Logs. Please contact your administrator.
//           </p>
//           <button
//             onClick={() => router.push('/')}
//             className="px-6 py-2 bg-amber-600 rounded-full hover:bg-amber-700 text-white"
//           >
//             Return to Dashboard
//           </button>
//         </div>
//         <Toaster position="top-right" />
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-black p-8 relative overflow-hidden">
//       {/* Animated Background Elements */}
//       <div className="absolute inset-0">
//         <div className="absolute top-20 left-10 w-96 h-96 bg-gradient-to-r from-purple-500/8 to-indigo-500/5 rounded-full blur-3xl animate-pulse"></div>
//         <div className="absolute bottom-20 right-10 w-80 h-80 bg-gradient-to-r from-cyan-500/6 to-purple-500/6 rounded-full blur-3xl animate-pulse delay-1000"></div>
//         <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-indigo-500/4 to-cyan-500/4 rounded-full blur-3xl animate-pulse delay-500"></div>
//       </div>

//       <div className="relative max-w-7xl mx-auto">
//         {/* Premium Header Section */}
//         <div className="mb-12">
//           <div className="flex items-center space-x-4 mb-6">
//             <div className="w-12 h-12 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/30">
//               <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
//                 <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
//               </svg>
//             </div>
//             <div>
//               <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-300 via-purple-400 to-indigo-300 bg-clip-text text-transparent">
//                 Audit Logs
//               </h1>
//               <p className="text-slate-400 text-lg mt-1">System activity tracking and monitoring</p>
//             </div>
//           </div>
          
//           <div className="flex items-center justify-between">
//             <div className="flex items-center space-x-6 text-sm">
//               <div className="flex items-center space-x-2 px-4 py-2 bg-slate-900/60 rounded-lg border border-slate-700/50 backdrop-blur-sm">
//                 <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
//                 <span className="text-slate-300">Total: <span className="text-indigo-300 font-semibold">{pagination.total}</span> records</span>
//               </div>
//               <div className="flex items-center space-x-2 px-4 py-2 bg-slate-900/60 rounded-lg border border-slate-700/50 backdrop-blur-sm">
//                 <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
//                 <span className="text-slate-300">Page <span className="text-indigo-300 font-semibold">{pagination.page}</span> of <span className="text-indigo-300 font-semibold">{pagination.totalPages}</span></span>
//               </div>
//               <div className="flex items-center space-x-2">
//                 <label className="text-slate-300 text-sm">Items per page:</label>
//                 <select
//                   value={pagination.limit}
//                   onChange={(e) => handleLimitChange(e.target.value)}
//                   className="px-2 py-1 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
//                 >
//                   <option value="10">10</option>
//                   <option value="25">25</option>
//                   <option value="50">50</option>
//                   <option value="100">100</option>
//                 </select>
//               </div>
//             </div>

//             <div className="flex items-center space-x-3">
//               <button
//                 onClick={clearFilters}
//                 className="px-4 py-2 text-slate-300 bg-slate-800/60 border border-slate-600/50 rounded-lg hover:bg-slate-700/60 hover:border-slate-500/50 transition-all duration-200 text-sm"
//               >
//                 Clear Filters
//               </button>
//               <button
//                 onClick={applyFilters}
//                 className="group relative px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold rounded-full shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transform hover:scale-105 transition-all duration-300 overflow-hidden"
//               >
//                 <div className="absolute inset-0 bg-gradient-to-r from-indigo-400 to-purple-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
//                 <div className="relative flex items-center space-x-2">
//                   <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
//                     <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
//                   </svg>
//                   <span>Search</span>
//                 </div>
//               </button>
//             </div>
//           </div>
//         </div>

//         {/* Advanced Filters Section */}
//         <div className="mb-8 backdrop-blur-xl bg-gradient-to-br from-slate-900/80 to-slate-800/60 rounded-2xl border border-indigo-400/20 shadow-2xl shadow-indigo-500/10 p-6">
//           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
//             <div>
//               <label className="block text-sm font-medium text-indigo-300 mb-2">User ID</label>
//               <input
//                 type="text"
//                 placeholder="Enter user ID"
//                 value={filters.user_id}
//                 onChange={(e) => handleFilterChange('user_id', e.target.value)}
//                 className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 placeholder-slate-400 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
//               />
//             </div>
//             <div>
//               <label className="block text-sm font-medium text-indigo-300 mb-2">Action</label>
//               <select
//                 value={filters.action}
//                 onChange={(e) => handleFilterChange('action', e.target.value)}
//                 className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
//               >
//                 <option value="">All Actions</option>
//                 <option value="CREATE">Create</option>
//                 <option value="UPDATE">Update</option>
//                 <option value="DELETE">Delete</option>
//                 <option value="LOGIN">Login</option>
//                 <option value="LOGOUT">Logout</option>
//               </select>
//             </div>
//             <div>
//               <label className="block text-sm font-medium text-indigo-300 mb-2">Table Name</label>
//               <input
//                 type="text"
//                 placeholder="Enter table name"
//                 value={filters.table_name}
//                 onChange={(e) => handleFilterChange('table_name', e.target.value)}
//                 className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 placeholder-slate-400 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
//               />
//             </div>
//             <div>
//               <label className="block text-sm font-medium text-indigo-300 mb-2">Start Date</label>
//               <input
//                 type="datetime-local"
//                 value={filters.start_date}
//                 onChange={(e) => handleFilterChange('start_date', e.target.value)}
//                 className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
//               />
//             </div>
//             <div>
//               <label className="block text-sm font-medium text-indigo-300 mb-2">End Date</label>
//               <input
//                 type="datetime-local"
//                 value={filters.end_date}
//                 onChange={(e) => handleFilterChange('end_date', e.target.value)}
//                 className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
//               />
//             </div>
//           </div>
//         </div>

//         {loading ? (
//           <div className="space-y-4">
//             {[...Array(pagination.limit)].map((_, i) => (
//               <div key={i} className="backdrop-blur-xl bg-gradient-to-r from-slate-900/60 to-slate-800/40 rounded-2xl border border-slate-700/30 shadow-xl p-6 animate-pulse">
//                 <div className="grid grid-cols-12 gap-4">
//                   <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
//                   <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
//                   <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
//                   <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
//                   <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
//                   <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
//                 </div>
//               </div>
//             ))}
//           </div>
//         ) : (
//           <>
//             {/* Luxury Table Container */}
//             <div className="backdrop-blur-xl bg-gradient-to-br from-slate-900/80 to-slate-800/60 rounded-2xl border border-indigo-400/20 shadow-2xl shadow-indigo-500/10 overflow-hidden">
              
//               {/* Table Header */}
//               <div className="bg-gradient-to-r from-slate-900/90 to-slate-800/90 border-b border-indigo-400/20">
//                 <div className="grid grid-cols-12 gap-4 px-8 py-4">
//                   <div className="col-span-2 font-semibold text-indigo-300 text-sm uppercase tracking-wider">User</div>
//                   <div className="col-span-2 font-semibold text-indigo-300 text-sm uppercase tracking-wider">Action</div>
//                   <div className="col-span-2 font-semibold text-indigo-300 text-sm uppercase tracking-wider">Table</div>
//                   <div className="col-span-2 font-semibold text-indigo-300 text-sm uppercase tracking-wider">Record ID</div>
//                   <div className="col-span-2 font-semibold text-indigo-300 text-sm uppercase tracking-wider">Timestamp</div>
//                   <div className="col-span-2 font-semibold text-indigo-300 text-sm uppercase tracking-wider">Details</div>
//                 </div>
//               </div>

//               {/* Data Rows */}
//               <div className="divide-y divide-slate-700/30">
//                 {auditLogsList.map((log, index) => (
//                   <div 
//                     key={log.id} 
//                     className={`grid grid-cols-12 gap-4 items-center px-8 py-6 hover:bg-gradient-to-r hover:from-indigo-500/5 hover:to-purple-500/5 transition-all duration-300 group ${
//                       index % 2 === 0 ? 'bg-slate-900/20' : 'bg-slate-800/20'
//                     }`}
//                   >
//                     <div className="col-span-2">
//                       <div className="flex items-center space-x-3">
//                         <div className="relative">
//                           <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400/20 to-purple-500/20 border border-indigo-400/30 flex items-center justify-center backdrop-blur-sm">
//                             <span className="text-xs font-semibold text-indigo-300">
//                               {log.user_id?.toString().charAt(0) || 'S'}
//                             </span>
//                           </div>
//                           <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-slate-900"></div>
//                         </div>
//                         <span className="text-slate-300 text-sm group-hover:text-slate-200 transition-colors">
//                           User #{log.user_id || 'System'}
//                         </span>
//                       </div>
//                     </div>
                    
//                     <div className="col-span-2">
//                       <span className={`inline-flex items-center px-3 py-1.5 rounded-full text-sm font-semibold bg-gradient-to-r ${getActionColor(log.action)} backdrop-blur-sm`}>
//                         {log.action}
//                       </span>
//                     </div>
                    
//                     <div className="col-span-2">
//                       <span className="text-amber-100 font-medium group-hover:text-amber-200 transition-colors">
//                         {log.table_name || 'N/A'}
//                       </span>
//                     </div>
                    
//                     <div className="col-span-2">
//                       <span className="text-slate-300 text-sm group-hover:text-slate-200 transition-colors font-mono">
//                         {log.record_id || 'N/A'}
//                       </span>
//                     </div>
                    
//                     <div className="col-span-2">
//                       <div className="text-xs">
//                         <div className="text-slate-300 group-hover:text-slate-200 transition-colors">
//                           {formatDateTime(log.timestamp)}
//                         </div>
//                       </div>
//                     </div>
                    
//                     <div className="col-span-2">
//                       {log.old_values || log.new_values ? (
//                         <button
//                           className="text-cyan-400 hover:text-cyan-300 text-sm font-medium bg-cyan-500/10 hover:bg-cyan-500/20 px-3 py-1 rounded-lg transition-all duration-200 border border-cyan-500/30"
//                           onClick={() => {
//                             const details = {
//                               old_values: log.old_values,
//                               new_values: log.new_values,
//                               ip_address: log.ip_address,
//                               user_agent: log.user_agent
//                             };
//                             alert(JSON.stringify(details, null, 2));
//                           }}
//                         >
//                           View Details
//                         </button>
//                       ) : (
//                         <span className="text-slate-500 italic text-sm">No details</span>
//                       )}
//                     </div>
//                   </div>
//                 ))}
//               </div>
//             </div>

//             {/* Premium Pagination */}
//             <div className="flex items-center justify-between mt-8 px-2">
//               <div className="flex items-center space-x-4">
//                 <div className="px-6 py-3 bg-gradient-to-r from-slate-900/80 to-slate-800/60 rounded-xl border border-slate-700/50 backdrop-blur-sm">
//                   <span className="text-slate-400 text-sm">
//                     Showing <span className="font-semibold text-indigo-300">{(pagination.page - 1) * pagination.limit + 1}</span> to{' '}
//                     <span className="font-semibold text-indigo-300">
//                       {Math.min(pagination.page * pagination.limit, pagination.total)}
//                     </span>{' '}
//                     of <span className="font-semibold text-indigo-300">{pagination.total}</span> results
//                   </span>
//                 </div>
//               </div>
              
//               <div className="flex items-center space-x-2">
//                 <button
//                   onClick={() => handlePageChange(pagination.page - 1)}
//                   disabled={pagination.page === 1}
//                   className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
//                     pagination.page === 1 
//                       ? 'text-slate-600 bg-slate-800/30 border border-slate-700/30 cursor-not-allowed' 
//                       : 'text-slate-300 bg-gradient-to-r from-slate-900/80 to-slate-800/60 border border-slate-700/50 hover:from-indigo-500/20 hover:to-purple-500/20 hover:border-indigo-400/50 hover:text-indigo-200 hover:scale-105 backdrop-blur-sm'
//                   }`}
//                 >
//                   Previous
//                 </button>
                
//                 <div className="flex items-center space-x-1">
//                   {Array.from({ length: Math.min(5, pagination.totalPages) }, (_, i) => {
//                     let pageNum;
//                     if (pagination.totalPages <= 5) {
//                       pageNum = i + 1;
//                     } else if (pagination.page <= 3) {
//                       pageNum = i + 1;
//                     } else if (pagination.page >= pagination.totalPages - 2) {
//                       pageNum = pagination.totalPages - 4 + i;
//                     } else {
//                       pageNum = pagination.page - 2 + i;
//                     }
                    
//                     return (
//                       <button
//                         key={pageNum}
//                         onClick={() => handlePageChange(pageNum)}
//                         className={`w-12 h-12 rounded-xl font-semibold transition-all duration-300 ${
//                           pagination.page === pageNum 
//                             ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg shadow-indigo-500/30 scale-110' 
//                             : 'text-slate-300 bg-gradient-to-r from-slate-900/80 to-slate-800/60 border border-slate-700/50 hover:from-indigo-500/20 hover:to-purple-500/20 hover:border-indigo-400/50 hover:text-indigo-200 hover:scale-105 backdrop-blur-sm'
//                         }`}
//                       >
//                         {pageNum}
//                       </button>
//                     );
//                   })}
//                 </div>
                
//                 <button
//                   onClick={() => handlePageChange(pagination.page + 1)}
//                   disabled={pagination.page === pagination.totalPages}
//                   className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
//                     pagination.page === pagination.totalPages 
//                       ? 'text-slate-600 bg-slate-800/30 border border-slate-700/30 cursor-not-allowed' 
//                       : 'text-slate-300 bg-gradient-to-r from-slate-900/80 to-slate-800/60 border border-slate-700/50 hover:from-indigo-500/20 hover:to-purple-500/20 hover:border-indigo-400/50 hover:text-indigo-200 hover:scale-105 backdrop-blur-sm'
//                   }`}
//                 >
//                   Next
//                 </button>
//               </div>
//             </div>
//           </>
//         )}
//       </div>
//       <Toaster />
//     </div>
//   );
// };

// export default AuditLogCom;





import React, { useEffect, useState, useContext } from 'react';
import AxiosInstance from "@/components/AxiosInstance";
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import { Toaster } from 'react-hot-toast';
import { AuthContext } from '@/components/AuthContext';

const AuditLogCom = () => {
  const router = useRouter();
  const { permissions = {} } = useContext(AuthContext);
  const [auditLogsList, setAuditLogsList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    performed_by_user_id: '',
    action: '',
    table_name: '',
    start_date: '',
    end_date: ''
  });
  const [pagination, setPagination] = useState({
    current_page: 1,
    limit: 10,
    total: 0,
    total_pages: 1,
    next: false,
    previous: false
  });

  const fetchAuditLogs = async (page = 1, limit = pagination.limit) => {
  setLoading(true);
  try {
    const params = {
      page,
      limit,
      ...Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== '')
      )
    };

    const response = await AxiosInstance.get('/audit-logs', { params });
    
    if (response.data.status?.toUpperCase() === 'SUCCESSFUL') {
      setAuditLogsList(response.data.result.data || []);
      setPagination(prev => ({
        ...prev,
        current_page: page,
        limit: limit,
        total: response.data.result.count,
        total_pages: Math.ceil(response.data.result.count / limit),
        next: page < Math.ceil(response.data.result.count / limit),
        previous: page > 1
      }));
    } else {
      throw new Error(response.data.message || 'Unknown error occurred');
    }
  } catch (error) {
    console.error("Audit log fetch error:", error);
    let errorMessage = 'Error fetching audit logs';
    
    if (error.response) {
      errorMessage = error.response.data?.message || 
                    error.response.data?.error || 
                    `Server error: ${error.response.status}`;
    } else if (error.request) {
      errorMessage = 'No response from server';
    } else {
      errorMessage = error.message || 'Request setup error';
    }
    
    toast.error(errorMessage, {
      position: "top-center",
      autoClose: 5000,
    });
  } finally {
    setLoading(false);
  }
};

  useEffect(() => {
    fetchAuditLogs(pagination.current_page);
  }, [pagination.current_page]);

  useEffect(() => {
    if (pagination.current_page === 1) {
      fetchAuditLogs(1, pagination.limit);
    } else {
      setPagination(prev => ({ ...prev, current_page: 1 }));
    }
  }, [pagination.limit]);

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.total_pages) {
      setPagination(prev => ({ ...prev, current_page: newPage }));
    }
  };

  const handleLimitChange = (e) => {
    const newLimit = parseInt(e.target.value);
    setPagination(prev => ({ 
      ...prev, 
      limit: newLimit,
      current_page: 1
    }));
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  const applyFilters = () => {
    setPagination(prev => ({ ...prev, current_page: 1 }));
    fetchAuditLogs(1);
  };

  const clearFilters = () => {
    setFilters({
      performed_by_user_id: '',
      action: '',
      table_name: '',
      start_date: '',
      end_date: ''
    });
    setPagination(prev => ({ ...prev, current_page: 1 }));
    fetchAuditLogs(1);
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getActionColor = (action) => {
    const colors = {
      'CREATE': 'from-green-500/20 to-emerald-500/20 text-green-300 border-green-500/30',
      'UPDATE': 'from-blue-500/20 to-indigo-500/20 text-blue-300 border-blue-500/30',
      'DELETE': 'from-red-500/20 to-rose-500/20 text-red-300 border-red-500/30',
      'LOGIN': 'from-amber-500/20 to-yellow-500/20 text-amber-300 border-amber-500/30',
      'LOGOUT': 'from-gray-500/20 to-slate-500/20 text-gray-300 border-gray-500/30'
    };
    return colors[action?.toUpperCase()] || 'from-slate-500/20 to-gray-500/20 text-slate-300 border-slate-500/30';
  };

  if (!permissions.read_auditlog) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center p-6">
        <div className="text-center p-8 max-w-md">
          <h2 className="text-2xl text-amber-400 mb-4">Access Denied</h2>
          <p className="text-gray-300 mb-6">
            You don't have permission to view Audit Logs. Please contact your administrator.
          </p>
          <button
            onClick={() => router.push('/')}
            className="px-6 py-2 bg-amber-600 rounded-full hover:bg-amber-700 text-white"
          >
            Return to Dashboard
          </button>
        </div>
        <Toaster position="top-right" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-black p-8 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-96 h-96 bg-gradient-to-r from-purple-500/8 to-indigo-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-80 h-80 bg-gradient-to-r from-cyan-500/6 to-purple-500/6 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-indigo-500/4 to-cyan-500/4 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      <div className="relative max-w-7xl mx-auto">
        {/* Premium Header Section */}
        <div className="mb-12">
          <div className="flex items-center space-x-4 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/30">
              <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-300 via-purple-400 to-indigo-300 bg-clip-text text-transparent">
                Audit Logs
              </h1>
              <p className="text-slate-400 text-lg mt-1">System activity tracking and monitoring</p>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6 text-sm">
              <div className="flex items-center space-x-2 px-4 py-2 bg-slate-900/60 rounded-lg border border-slate-700/50 backdrop-blur-sm">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-slate-300">Total: <span className="text-indigo-300 font-semibold">{pagination.total}</span> records</span>
              </div>
              <div className="flex items-center space-x-2 px-4 py-2 bg-slate-900/60 rounded-lg border border-slate-700/50 backdrop-blur-sm">
                <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                <span className="text-slate-300">Page <span className="text-indigo-300 font-semibold">{pagination.current_page}</span> of <span className="text-indigo-300 font-semibold">{pagination.total_pages}</span></span>
              </div>
              <div className="flex items-center space-x-2">
                <label className="text-slate-300 text-sm">Items per page:</label>
                <select
                  value={pagination.limit}
                  onChange={handleLimitChange}
                  className="px-2 py-1 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
                >
                  <option value="10">10</option>
                  <option value="25">25</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                </select>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <button
                onClick={clearFilters}
                className="px-4 py-2 text-slate-300 bg-slate-800/60 border border-slate-600/50 rounded-lg hover:bg-slate-700/60 hover:border-slate-500/50 transition-all duration-200 text-sm"
              >
                Clear Filters
              </button>
              <button
                onClick={applyFilters}
                className="group relative px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold rounded-full shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transform hover:scale-105 transition-all duration-300 overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-400 to-purple-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div className="relative flex items-center space-x-2">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                  </svg>
                  <span>Search</span>
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Advanced Filters Section */}
        <div className="mb-8 backdrop-blur-xl bg-gradient-to-br from-slate-900/80 to-slate-800/60 rounded-2xl border border-indigo-400/20 shadow-2xl shadow-indigo-500/10 p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <div>
              <label className="block text-sm font-medium text-indigo-300 mb-2">User ID</label>
              <input
                type="text"
                placeholder="Enter user ID"
                value={filters.performed_by_user_id}
                onChange={(e) => handleFilterChange('performed_by_user_id', e.target.value)}
                className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 placeholder-slate-400 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-indigo-300 mb-2">Action</label>
              <select
                value={filters.action}
                onChange={(e) => handleFilterChange('action', e.target.value)}
                className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
              >
                <option value="">All Actions</option>
                <option value="INSERT">INSERT</option>
                <option value="UPDATE">UPDATE</option>
                <option value="DELETE">DELETE</option>
                <option value="LOGIN">Login</option>
                <option value="LOGOUT">Logout</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-indigo-300 mb-2">Table Name</label>
              <input
                type="text"
                placeholder="Enter table name"
                value={filters.table_name}
                onChange={(e) => handleFilterChange('table_name', e.target.value)}
                className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 placeholder-slate-400 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-indigo-300 mb-2">Start Date</label>
              <input
                type="datetime-local"
                value={filters.start_date}
                onChange={(e) => handleFilterChange('start_date', e.target.value)}
                className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-indigo-300 mb-2">End Date</label>
              <input
                type="datetime-local"
                value={filters.end_date}
                onChange={(e) => handleFilterChange('end_date', e.target.value)}
                className="w-full px-4 py-2 bg-slate-800/50 border border-slate-600/50 rounded-lg text-slate-200 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200"
              />
            </div>
          </div>
        </div>

        {loading ? (
          <div className="space-y-4">
            {[...Array(pagination.limit)].map((_, i) => (
              <div key={i} className="backdrop-blur-xl bg-gradient-to-r from-slate-900/60 to-slate-800/40 rounded-2xl border border-slate-700/30 shadow-xl p-6 animate-pulse">
                <div className="grid grid-cols-12 gap-4">
                  <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
                  <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
                  <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
                  <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
                  <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
                  <div className="col-span-2 h-6 bg-slate-700/50 rounded-lg"></div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <>
            {/* Luxury Table Container */}
            <div className="backdrop-blur-xl bg-gradient-to-br from-slate-900/80 to-slate-800/60 rounded-2xl border border-indigo-400/20 shadow-2xl shadow-indigo-500/10 overflow-hidden">
              
              {/* Table Header */}
              <div className="bg-gradient-to-r from-slate-900/90 to-slate-800/90 border-b border-indigo-400/20">
                <div className="grid grid-cols-12 gap-3 px-6 py-3">
                  <div className="col-span-1 font-semibold text-indigo-300 text-xs uppercase tracking-wider text-center">#</div>
                  <div className="col-span-2 font-semibold text-indigo-300 text-xs uppercase tracking-wider text-left">User</div>
                  <div className="col-span-1 font-semibold text-indigo-300 text-xs uppercase tracking-wider text-center">Action</div>
                  <div className="col-span-2 font-semibold text-indigo-300 text-xs uppercase tracking-wider text-left">Table</div>
                  <div className="col-span-2 font-semibold text-indigo-300 text-xs uppercase tracking-wider text-center">Record ID</div>
                  <div className="col-span-2 font-semibold text-indigo-300 text-xs uppercase tracking-wider text-center">Timestamp</div>
                  <div className="col-span-2 font-semibold text-indigo-300 text-xs uppercase tracking-wider text-center">Details</div>
                </div>
              </div>

              {/* Data Rows */}
              <div className="divide-y divide-slate-700/20">
                {auditLogsList.map((log, index) => (
                  <div 
                    key={log.id} 
                    className={`grid grid-cols-12 gap-3 items-center px-6 py-3 hover:bg-gradient-to-r hover:from-indigo-500/8 hover:to-purple-500/8 transition-all duration-200 group cursor-pointer ${
                      index % 2 === 0 ? 'bg-slate-900/10' : 'bg-slate-800/15'
                    }`}
                  >
                    {/* Serial Number */}
                    <div className="col-span-1 text-center">
                      <span className="text-slate-400 text-xs font-medium bg-slate-800/30 px-2 py-1 rounded-md">
                        {index + 1 + (pagination.current_page - 1) * pagination.limit}
                      </span>
                    </div>
                    
                    {/* User */}
                    <div className="col-span-2 flex items-center space-x-2">
                      <div className="relative">
                        <div className="w-6 h-6 rounded-full bg-gradient-to-br from-indigo-400/30 to-purple-500/30 border border-indigo-400/40 flex items-center justify-center">
                          <span className="text-xs font-bold text-indigo-200">
                            {log.performed_by_user_id?.toString().charAt(0) || 'S'}
                          </span>
                        </div>
                        <div className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-green-400 rounded-full border border-slate-900"></div>
                      </div>
                      <span className="text-slate-300 text-xs font-medium group-hover:text-slate-200 transition-colors truncate">
                        User #{log.performed_by_user_id || 'System'}
                      </span>
                    </div>
                    
                    {/* Action */}
                    <div className="col-span-1 flex justify-center">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold bg-gradient-to-r ${getActionColor(log.action)} backdrop-blur-sm shadow-sm`}>
                        {log.action}
                      </span>
                    </div>
                    
                    {/* Table */}
                    <div className="col-span-2">
                      <span className="text-amber-200 font-medium text-xs group-hover:text-amber-100 transition-colors bg-amber-500/10 px-2 py-1 rounded-md border border-amber-500/20 truncate block">
                        {log.table_name || 'N/A'}
                      </span>
                    </div>
                    
                    {/* Record ID */}
                    <div className="col-span-2 text-center">
                      <span className="text-slate-300 text-xs group-hover:text-slate-200 transition-colors font-mono bg-slate-700/30 px-2 py-1 rounded border border-slate-600/30">
                        {log.record_id || 'N/A'}
                      </span>
                    </div>
                    
                    {/* Timestamp */}
                    <div className="col-span-2 text-center">
                      <div className="text-xs bg-slate-800/40 px-2 py-1 rounded border border-slate-700/30">
                        <div className="text-slate-300 group-hover:text-slate-200 transition-colors">
                          {formatDateTime(log.timestamp)}
                        </div>
                      </div>
                    </div>
                    
                    {/* Details */}
                    <div className="col-span-2 text-center">
                      {log.old_values || log.new_values ? (
                        <button
                          className="text-cyan-300 hover:text-cyan-200 text-xs font-medium bg-cyan-500/15 hover:bg-cyan-500/25 px-2 py-1 rounded-md transition-all duration-200 border border-cyan-500/40 hover:border-cyan-400/60 shadow-sm hover:shadow-cyan-500/20"
                          onClick={() => {
                            const details = {
                              old_values: log.old_values,
                              new_values: log.new_values,
                              ip_address: log.ip_address,
                              user_agent: log.user_agent
                            };
                            alert(JSON.stringify(details, null, 2));
                          }}
                        >
                          View
                        </button>
                      ) : (
                        <span className="text-slate-500 italic text-xs bg-slate-800/20 px-2 py-1 rounded border border-slate-700/20">—</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Enhanced Pagination */}
            <div className="flex flex-col md:flex-row justify-between items-center mt-16 gap-4">
              <div className="text-gray-400 text-sm">
                Page {pagination.current_page} of {pagination.total_pages} • Total {pagination.total} logs
              </div>
              
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handlePageChange(1)}
                  disabled={pagination.current_page === 1}
                  className="p-2 rounded-full bg-gray-100 hover:bg-gray-500 disabled:opacity-50 transition-colors"
                  aria-label="First page"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M15.707 15.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 010 1.414zm-6 0a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 1.414L5.414 10l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
                  </svg>
                </button>
                
                <button
                  onClick={() => handlePageChange(pagination.current_page - 1)}
                  disabled={!pagination.previous}
                  className="p-2 rounded-full bg-gray-100 hover:bg-gray-500 disabled:opacity-50 transition-colors"
                  aria-label="Previous page"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
                
                <div className="flex items-center gap-1">
                  {Array.from({ length: Math.min(5, pagination.total_pages) }, (_, i) => {
                    let pageNum;
                    if (pagination.total_pages <= 5) {
                      pageNum = i + 1;
                    } else if (pagination.current_page <= 3) {
                      pageNum = i + 1;
                    } else if (pagination.current_page >= pagination.total_pages - 2) {
                      pageNum = pagination.total_pages - 4 + i;
                    } else {
                      pageNum = pagination.current_page - 2 + i;
                    }
                    
                    return (
                      <button
                        key={pageNum}
                        onClick={() => handlePageChange(pageNum)}
                        className={`w-8 h-8 rounded-full text-sm transition-colors ${
                          pagination.current_page === pageNum
                            ? 'bg-amber-600 text-white'
                            : 'bg-gray-800 hover:bg-gray-700 text-gray-300'
                        }`}
                        aria-label={`Page ${pageNum}`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                </div>
                
                <button
                  onClick={() => handlePageChange(pagination.current_page + 1)}
                  disabled={!pagination.next}
                  className="p-2 rounded-full bg-gray-100 hover:bg-gray-500 disabled:opacity-50 transition-colors"
                  aria-label="Next page"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
                
                <button
                  onClick={() => handlePageChange(pagination.total_pages)}
                  disabled={pagination.current_page === pagination.total_pages}
                  className="p-2 rounded-full bg-gray-100 hover:bg-gray-500 disabled:opacity-50 transition-colors"
                  aria-label="Last page"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10.293 15.707a1 1 0 010-1.414L14.586 10l-4.293-4.293a1 1 0 111.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    <path fillRule="evenodd" d="M4.293 15.707a1 1 0 010-1.414L8.586 10 4.293 5.707a1 1 0 011.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </>
        )}
      </div>
      <Toaster />
    </div>
  );
};

export default AuditLogCom;