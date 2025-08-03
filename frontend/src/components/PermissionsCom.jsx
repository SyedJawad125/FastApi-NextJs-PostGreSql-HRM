import React, { useEffect, useState, useContext } from 'react';
import AxiosInstance from "@/components/AxiosInstance";
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import { Toaster } from 'react-hot-toast';
import { AuthContext } from '@/components/AuthContext';

const PermissionsCom = () => {
  const router = useRouter();
  const { permissions = {} } = useContext(AuthContext);
  const [permissionsList, setPermissionsList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0,
    totalPages: 1
  });

  const fetchPermissions = async (page = 1) => {
    setLoading(true);
    try {
      const response = await AxiosInstance.get('/permissions/get_admin', {
        params: {
          page,
          limit: pagination.limit
        }
      });
      if (response.data.status === 'SUCCESSFUL') {
        setPermissionsList(response.data.result.data);
        setPagination(prev => ({
          ...prev,
          page,
          total: response.data.result.count,
          totalPages: Math.ceil(response.data.result.count / pagination.limit)
        }));
      }
    } catch (error) {
      console.error('Error fetching permissions:', error);
      toast.error('Error fetching permissions');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPermissions(pagination.page);
  }, [pagination.page]);

  const updatePermission = (id) => {
    router.push(`/UpdatePermissionPage?id=${id}`);
  };

  const deletePermission = async (id) => {
    try {
      const res = await AxiosInstance.delete(`/permissions/${id}`);
      if (res?.data?.status === "SUCCESSFUL") {
        toast.success(res.data.message || 'Permission deleted successfully!');

        const newTotal = pagination.total - 1;
        const newTotalPages = Math.ceil(newTotal / pagination.limit);
        const newPage = pagination.page > newTotalPages ? newTotalPages : pagination.page;

        setPagination(prev => ({
          ...prev,
          page: newPage
        }));
      }
    } catch (error) {
      if (error.response?.status === 404) {
        toast.error('Permission not found');
      } else {
        const errorMessage = error.response?.data?.detail || 'Error deleting permission';
        toast.error(errorMessage);
      }
    }
  };

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.totalPages) {
      fetchPermissions(newPage);
    }
  };

  // Check for read permissions
  if (!permissions.read_permission) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center p-6">
        <div className="text-center p-8 max-w-md">
          <h2 className="text-2xl text-amber-400 mb-4">Access Denied</h2>
          <p className="text-gray-300 mb-6">
            You don't have permission to view Permissions. Please contact your administrator.
          </p>
          <button
            onClick={() => router.push('/')}
            className="px-6 py-2 bg-amber-600 rounded-full hover:bg-amber-700 text-white"
          >
            Return to Dashboard
          </button>
        </div>
        <Toaster position="top-right" autoClose={2000} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-12">
          <h1 className="text-3xl font-bold text-white mb-2">Permissions Management</h1>
          <div className="flex items-center text-sm text-gray-400">
            <span>Total: {pagination.total} records</span>
            <span className="mx-2">•</span>
            <span>Page {pagination.page} of {pagination.totalPages}</span>
          </div>
        </div>

        {permissions.create_permission && (
          <button
            onClick={() => router.push('/AddPermissionPage')}
            className="px-6 py-3 -mt-4 mb-4 border border-amber-500 text-amber-500 rounded-full hover:bg-amber-500 hover:text-black"
          >
            Add Permission
          </button>
        )}

        {loading ? (
          <div className="space-y-4">
            {[...Array(pagination.limit)].map((_, i) => (
              <div key={i} className="grid grid-cols-12 gap-4 p-6 bg-gray-900 rounded-lg shadow-lg animate-pulse">
                <div className="col-span-2 h-6 bg-gray-800 rounded"></div>
                <div className="col-span-2 h-6 bg-gray-800 rounded"></div>
                <div className="col-span-3 h-6 bg-gray-800 rounded"></div>
                <div className="col-span-2 h-6 bg-gray-800 rounded"></div>
                <div className="col-span-2 h-6 bg-gray-800 rounded"></div>
                <div className="col-span-1 h-6 bg-gray-800 rounded"></div>
              </div>
            ))}
          </div>
        ) : (
          <>
            {/* Table Header */}
            <div className="grid grid-cols-12 gap-4 px-6 py-3 bg-gray-900 rounded-t-lg border-b border-gray-800">
              <div className="col-span-2 font-medium text-gray-300">Code</div>
              <div className="col-span-2 font-medium text-gray-300">Name</div>
              <div className="col-span-3 font-medium text-gray-300">Description</div>
              <div className="col-span-2 font-medium text-gray-300">Module</div>
              <div className="col-span-2 font-medium text-gray-300">Created By</div>
              <div className="col-span-1 font-medium text-gray-300 text-right">Actions</div>
            </div>

            {/* Data Rows */}
            <div className="bg-gray-900 rounded-b-lg shadow-lg divide-y divide-gray-800">
              {permissionsList.map((permission) => (
                <div key={permission.id} className="grid grid-cols-12 gap-4 items-center p-6 hover:bg-gray-800 transition-colors">
                  <div className="col-span-2 font-medium text-white">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-900/50 text-purple-300 border border-purple-800">
                      {permission.code}
                    </span>
                  </div>
                  <div className="col-span-2 text-gray-300 ">
                    {permission.name}
                  </div>
                  <div className="col-span-3 text-gray-300 text-sm">
                    <div className="max-w-xs truncate" title={permission.description}>
                      {permission.description}
                    </div>
                  </div>
                  <div className="col-span-2 text-gray-300">
                    {permission.module_name ? (
                      <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-blue-900/50 text-blue-300 border border-blue-800">
                        {permission.module_name}
                      </span>
                    ) : (
                      <span className="text-gray-500">N/A</span>
                    )}
                  </div>
                  <div className="col-span-2 text-gray-300">
                    <div className="flex items-center">
                      <span className="inline-block w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center mr-2">
                        <span className="text-xs text-gray-300">
                          {permission.created_by_user_id?.toString().charAt(0) || 'S'}
                        </span>
                      </span>
                      User #{permission.created_by_user_id || 'System'}
                    </div>
                  </div>
                  <div className="col-span-1 flex justify-end space-x-2">
                    {permissions.update_permission && (
                      <button 
                        onClick={() => updatePermission(permission.id)}
                        className="p-2 text-gray-400 hover:text-indigo-400 hover:bg-gray-700 rounded-full transition-colors"
                        title="Edit Permission"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                        </svg>
                      </button>
                    )}
                    {permissions.delete_permission && (
                      <button 
                        onClick={() => deletePermission(permission.id)}
                        className="p-2 text-gray-400 hover:text-red-400 hover:bg-gray-700 rounded-full transition-colors"
                        title="Delete Permission"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-between mt-6 px-2">
              <div className="text-sm text-gray-400">
                Showing <span className="font-medium text-white">{(pagination.page - 1) * pagination.limit + 1}</span> to{' '}
                <span className="font-medium text-white">
                  {Math.min(pagination.page * pagination.limit, pagination.total)}
                </span>{' '}
                of <span className="font-medium text-white">{pagination.total}</span> results
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handlePageChange(pagination.page - 1)}
                  disabled={pagination.page === 1}
                  className={`px-4 py-2 border rounded-md ${pagination.page === 1 ? 'text-gray-600 border-gray-700 cursor-not-allowed' : 'text-gray-300 border-gray-600 hover:bg-gray-800'}`}
                >
                  Previous
                </button>
                <div className="flex space-x-1">
                  {Array.from({ length: Math.min(5, pagination.totalPages) }, (_, i) => {
                    let pageNum;
                    if (pagination.totalPages <= 5) {
                      pageNum = i + 1;
                    } else if (pagination.page <= 3) {
                      pageNum = i + 1;
                    } else if (pagination.page >= pagination.totalPages - 2) {
                      pageNum = pagination.totalPages - 4 + i;
                    } else {
                      pageNum = pagination.page - 2 + i;
                    }
                    
                    return (
                      <button
                        key={pageNum}
                        onClick={() => handlePageChange(pageNum)}
                        className={`w-10 h-10 rounded-md ${pagination.page === pageNum ? 'bg-indigo-600 text-white' : 'text-gray-300 border border-gray-600 hover:bg-gray-800'}`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                </div>
                <button
                  onClick={() => handlePageChange(pagination.page + 1)}
                  disabled={pagination.page === pagination.totalPages}
                  className={`px-4 py-2 border rounded-md ${pagination.page === pagination.totalPages ? 'text-gray-600 border-gray-700 cursor-not-allowed' : 'text-gray-300 border-gray-600 hover:bg-gray-800'}`}
                >
                  Next
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

export default PermissionsCom;