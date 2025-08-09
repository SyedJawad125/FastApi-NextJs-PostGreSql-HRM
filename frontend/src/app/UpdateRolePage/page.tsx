'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import AxiosInstance from "@/components/AxiosInstance";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

interface Permission {
  id: number;
  name: string;
  description: string;
  code: string;
  module_name?: string;
}

interface Role {
  id: number;
  name: string;
  description: string;
  code: string;
  permissions: Permission[];
}

export default function UpdateRole() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const roleId = searchParams.get('id');

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    code: '',
    permission_ids: [] as number[],
  });

  const [permissions, setPermissions] = useState<Permission[]>([]);
  const [loading, setLoading] = useState(false);
  const [fetchingData, setFetchingData] = useState(true);

  // Fetch role data and permissions
  useEffect(() => {
    const fetchData = async () => {
      if (!roleId) {
        toast.error('Role ID not provided');
        router.push('/RolesPage');
        return;
      }

      setFetchingData(true);
      try {
        // Fetch permissions
        const permissionsResponse = await AxiosInstance.get('/permissions/get_admin_without_paginated');
        const permissionsData = permissionsResponse.data?.result?.data ?? [];
        setPermissions(permissionsData);

        // Fetch role data
        const roleResponse = await AxiosInstance.get(`/roles/${roleId}`);
        const roleData = roleResponse.data?.result || roleResponse.data?.data || roleResponse.data;
        
        if (roleData) {
          setFormData({
            name: roleData.name || '',
            description: roleData.description || '',
            code: roleData.code || '',
            permission_ids: roleData.permissions ? roleData.permissions.map((p: Permission) => p.id) : [],
          });
        } else {
          toast.error('Role not found');
          router.push('/RolesPage');
        }
      } catch (error: any) {
        console.error('Error fetching data:', error);
        const errorMessage = error.response?.data?.detail || 'Failed to load role data';
        toast.error(errorMessage);
        setTimeout(() => router.push('/RolesPage'), 2000);
      } finally {
        setFetchingData(false);
      }
    };

    fetchData();
  }, [roleId, router]);

  // Handle input change for text fields
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle permission checkbox change
  const handlePermissionToggle = (id: number) => {
    setFormData((prev) => {
      const isSelected = prev.permission_ids.includes(id);
      return {
        ...prev,
        permission_ids: isSelected
          ? prev.permission_ids.filter(pid => pid !== id)
          : [...prev.permission_ids, id],
      };
    });
  };

  // Submit form
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name.trim() || !formData.description.trim() || !formData.code.trim()) {
      toast.error('Please fill in all required fields.');
      return;
    }

    setLoading(true);
    try {
      await AxiosInstance.patch(`/roles/${roleId}`, {
        name: formData.name.trim(),
        description: formData.description.trim(),
        code: formData.code.trim(),
        permission_ids: formData.permission_ids,
      });

      toast.success('Role updated successfully!');
      setTimeout(() => {
        router.push('/RolesPage');
      }, 1500);
    } catch (error: any) {
      console.error('Error updating role:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to update role.';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Loading state
  if (fetchingData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-black py-16 px-4 relative overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-96 h-96 bg-gradient-to-r from-amber-500/10 to-orange-500/5 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-10 w-80 h-80 bg-gradient-to-r from-yellow-500/8 to-amber-500/8 rounded-full blur-3xl animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-amber-500/5 to-yellow-500/5 rounded-full blur-3xl animate-pulse delay-500"></div>
        </div>

        <ToastContainer />
        
        <div className="relative max-w-4xl mx-auto">
          {/* Loading Container */}
          <div className="backdrop-blur-2xl bg-gradient-to-br from-slate-900/90 via-slate-800/80 to-slate-900/90 rounded-3xl border border-amber-400/30 shadow-2xl shadow-amber-500/20 p-10 relative overflow-hidden">
            <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-amber-500/20 via-yellow-500/20 to-amber-500/20 animate-pulse opacity-40"></div>
            <div className="absolute inset-[1px] rounded-3xl bg-gradient-to-br from-slate-900/95 to-slate-800/90 backdrop-blur-2xl"></div>
            
            <div className="relative z-10 animate-pulse space-y-6">
              <div className="text-center mb-10">
                <div className="w-16 h-16 bg-amber-400/20 rounded-full mx-auto mb-6"></div>
                <div className="h-8 bg-slate-800 rounded w-64 mx-auto mb-3"></div>
                <div className="h-4 bg-slate-800 rounded w-48 mx-auto"></div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="h-20 bg-slate-800/50 rounded-xl"></div>
                <div className="h-20 bg-slate-800/50 rounded-xl"></div>
              </div>
              <div className="h-32 bg-slate-800/50 rounded-xl"></div>
              <div className="space-y-4">
                <div className="h-6 bg-slate-800/50 rounded w-32"></div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {[...Array(6)].map((_, i) => (
                    <div key={i} className="h-16 bg-slate-800/50 rounded-xl"></div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-black py-16 px-4 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-96 h-96 bg-gradient-to-r from-amber-500/10 to-orange-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-80 h-80 bg-gradient-to-r from-yellow-500/8 to-amber-500/8 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-amber-500/5 to-yellow-500/5 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      <ToastContainer />
      
      <div className="relative max-w-4xl mx-auto">
        {/* Luxury Glassmorphism Container */}
        <div className="backdrop-blur-2xl bg-gradient-to-br from-slate-900/90 via-slate-800/80 to-slate-900/90 rounded-3xl border border-amber-400/30 shadow-2xl shadow-amber-500/20 p-10 relative overflow-hidden">
          
          {/* Animated Border Glow */}
          <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-amber-500/20 via-yellow-500/20 to-amber-500/20 animate-pulse opacity-40"></div>
          <div className="absolute inset-[1px] rounded-3xl bg-gradient-to-br from-slate-900/95 to-slate-800/90 backdrop-blur-2xl"></div>
          
          <div className="relative z-10">
            {/* Premium Header */}
            <div className="text-center mb-10">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-amber-400 to-yellow-500 rounded-full shadow-2xl shadow-amber-500/50 mb-6">
                <svg className="w-8 h-8 text-slate-900" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </div>
              <h2 className="text-4xl font-bold bg-gradient-to-r from-amber-300 via-yellow-400 to-amber-300 bg-clip-text text-transparent mb-3 tracking-tight">
                Update Role
              </h2>
              <p className="text-slate-400 text-lg">Modify existing role permissions and details</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-8">
              
              {/* Input Fields Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Role Name */}
                <div className="space-y-3">
                  <label className="text-amber-300 font-semibold text-sm uppercase tracking-wider flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                    Role Name *
                  </label>
                  <div className="relative group">
                    <input
                      type="text"
                      name="name"
                      placeholder="Enter role name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      className="w-full px-6 py-4 rounded-xl bg-slate-900/60 border-2 border-slate-700/50 text-amber-100 placeholder-slate-500 focus:border-amber-400 focus:bg-slate-900/80 focus:shadow-lg focus:shadow-amber-500/20 transition-all duration-300 outline-none backdrop-blur-sm"
                    />
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-amber-500/0 to-yellow-500/0 group-focus-within:from-amber-500/10 group-focus-within:to-yellow-500/10 transition-all duration-300 pointer-events-none"></div>
                  </div>
                </div>

                {/* Role Code */}
                <div className="space-y-3">
                  <label className="text-amber-300 font-semibold text-sm uppercase tracking-wider flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                    Role Code *
                  </label>
                  <div className="relative group">
                    <input
                      type="text"
                      name="code"
                      placeholder="Enter role code"
                      value={formData.code}
                      onChange={handleChange}
                      required
                      className="w-full px-6 py-4 rounded-xl bg-slate-900/60 border-2 border-slate-700/50 text-amber-100 placeholder-slate-500 focus:border-amber-400 focus:bg-slate-900/80 focus:shadow-lg focus:shadow-amber-500/20 transition-all duration-300 outline-none backdrop-blur-sm"
                    />
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-amber-500/0 to-yellow-500/0 group-focus-within:from-amber-500/10 group-focus-within:to-yellow-500/10 transition-all duration-300 pointer-events-none"></div>
                  </div>
                </div>
              </div>

              {/* Description */}
              <div className="space-y-3">
                <label className="text-amber-300 font-semibold text-sm uppercase tracking-wider flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                  </svg>
                  Description *
                </label>
                <div className="relative group">
                  <textarea
                    name="description"
                    placeholder="Enter detailed role description"
                    value={formData.description}
                    onChange={handleChange}
                    rows={4}
                    required
                    className="w-full px-6 py-4 rounded-xl bg-slate-900/60 border-2 border-slate-700/50 text-amber-100 placeholder-slate-500 focus:border-amber-400 focus:bg-slate-900/80 focus:shadow-lg focus:shadow-amber-500/20 transition-all duration-300 outline-none backdrop-blur-sm resize-none"
                  />
                  <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-amber-500/0 to-yellow-500/0 group-focus-within:from-amber-500/10 group-focus-within:to-yellow-500/10 transition-all duration-300 pointer-events-none"></div>
                </div>
              </div>

              {/* Premium Permissions Section */}
              <div className="space-y-6">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-gradient-to-r from-amber-400 to-yellow-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-slate-900" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-amber-300">Permissions</h3>
                  <div className="h-px bg-gradient-to-r from-amber-500/50 to-transparent flex-1 ml-4"></div>
                  <div className="text-sm text-slate-400">
                    {formData.permission_ids.length} selected
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {permissions.map((perm) => (
                    <label
                      key={perm.id}
                      className="group relative cursor-pointer block"
                    >
                      <div className={`p-5 rounded-xl border-2 backdrop-blur-sm transition-all duration-300 ${
                        formData.permission_ids.includes(perm.id)
                          ? 'bg-gradient-to-br from-amber-500/20 to-yellow-500/20 border-amber-400/60 shadow-lg shadow-amber-500/25'
                          : 'bg-slate-900/40 border-slate-700/40 hover:border-amber-400/40 hover:bg-slate-900/60 hover:shadow-lg hover:shadow-amber-500/10'
                      }`}>
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-semibold text-amber-100 group-hover:text-amber-200 transition-colors">
                            {perm.name}
                          </span>
                          <div className={`relative w-6 h-6 rounded-full border-2 transition-all duration-300 ${
                            formData.permission_ids.includes(perm.id)
                              ? 'bg-gradient-to-r from-amber-400 to-yellow-500 border-amber-400 shadow-lg shadow-amber-500/50'
                              : 'border-slate-500 bg-slate-800/50 group-hover:border-amber-400'
                          }`}>
                            {formData.permission_ids.includes(perm.id) && (
                              <svg className="w-4 h-4 text-slate-900 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                              </svg>
                            )}
                          </div>
                        </div>
                        {perm.description && (
                          <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors">
                            {perm.description}
                          </p>
                        )}
                      </div>
                      <input
                        type="checkbox"
                        checked={formData.permission_ids.includes(perm.id)}
                        onChange={() => handlePermissionToggle(perm.id)}
                        className="sr-only"
                      />
                    </label>
                  ))}
                </div>
              </div>

              {/* Premium Submit Button Group */}
              <div className="flex justify-center space-x-6 pt-8">
                <button
                  type="button"
                  onClick={() => router.push('/RolesPage')}
                  className="px-8 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white font-semibold rounded-xl border border-slate-600 hover:border-slate-500 transition-all duration-300 shadow-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className={`group relative px-12 py-4 bg-gradient-to-r from-amber-500 via-yellow-500 to-amber-500 text-slate-900 font-bold text-lg rounded-full shadow-2xl shadow-amber-500/50 hover:shadow-amber-500/70 transform hover:scale-105 transition-all duration-300 overflow-hidden ${
                    loading ? 'opacity-50 cursor-not-allowed' : ''
                  }`}
                >
                  {/* Button Background Animation */}
                  <div className="absolute inset-0 bg-gradient-to-r from-amber-400 via-yellow-400 to-amber-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  
                  {/* Button Content */}
                  <div className="relative flex items-center space-x-3">
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                    <span>{loading ? 'Updating...' : 'Update Role'}</span>
                  </div>
                </button>
              </div>

            </form>
          </div>
        </div>

        {/* Elegant Footer */}
        <div className="text-center mt-8">
          <p className="text-slate-500 flex items-center justify-center space-x-2">
            <svg className="w-4 h-4 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>Secure Enterprise Role Management</span>
          </p>
        </div>
      </div>
    </div>
  );
}