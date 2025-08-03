'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import AxiosInstance from "@/components/AxiosInstance";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const AddPermission = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    code: '',
    module_name: ''
  });
  const [loading, setLoading] = useState(false);

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Generate code from name automatically
  const generateCode = (name: string) => {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '') // Remove special characters
      .replace(/\s+/g, '_') // Replace spaces with underscores
      .trim();
  };

  // Handle name change and auto-generate code
  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setFormData(prev => ({
      ...prev,
      name: value,
      code: generateCode(value)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Validate required fields
      if (!formData.name.trim() || !formData.description.trim() || !formData.code.trim()) {
        toast.error('Please fill in all required fields.');
        setLoading(false);
        return;
      }

      const response = await AxiosInstance.post('/permissions', {
        name: formData.name.trim(),
        description: formData.description.trim(),
        code: formData.code.trim(),
        module_name: formData.module_name.trim() || null
      });
      
      if (response) {
        toast.success('Permission added successfully!');
        setTimeout(() => {
          router.push('/permissionspage');
        }, 1500);
      }
    } catch (error: any) {
      console.error('Error submitting the form:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to add permission.';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-black to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <ToastContainer />
      <div className="max-w-2xl mx-auto">
        <div className="bg-gray-950 rounded-2xl shadow-2xl overflow-hidden border border-gray-800">
          
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-600 to-purple-800 px-6 py-5 shadow-md">
            <h2 className="text-3xl font-bold text-white">Add New Permission</h2>
            <p className="mt-1 text-purple-100">Create a new system permission below</p>
          </div>
          
          {/* Form */}
          <form className="p-6 space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-6">
              
              {/* Permission Name */}
              <div>
                <label htmlFor="name" className="block text-sm font-semibold text-purple-400 mb-1">
                  Permission Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  className="w-full px-4 py-2 rounded-lg border border-gray-700 bg-black text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
                  value={formData.name}
                  onChange={handleNameChange}
                  required
                  maxLength={50}
                  placeholder="e.g., Read User Data"
                />
                <p className="mt-1 text-xs text-gray-400">Max 50 characters. This will auto-generate the code.</p>
              </div>

              {/* Permission Code */}
              <div>
                <label htmlFor="code" className="block text-sm font-semibold text-purple-400 mb-1">
                  Permission Code <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  id="code"
                  name="code"
                  className="w-full px-4 py-2 rounded-lg border border-gray-700 bg-black text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
                  value={formData.code}
                  onChange={handleInputChange}
                  required
                  maxLength={50}
                  placeholder="e.g., read_user_data"
                />
                <p className="mt-1 text-xs text-gray-400">Max 50 characters. Use lowercase letters, numbers, and underscores only.</p>
              </div>

              {/* Description */}
              <div>
                <label htmlFor="description" className="block text-sm font-semibold text-purple-400 mb-1">
                  Description <span className="text-red-500">*</span>
                </label>
                <textarea
                  id="description"
                  name="description"
                  rows={4}
                  className="w-full px-4 py-2 rounded-lg border border-gray-700 bg-black text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition resize-none"
                  value={formData.description}
                  onChange={handleInputChange}
                  required
                  maxLength={500}
                  placeholder="Describe what this permission allows users to do..."
                />
                <p className="mt-1 text-xs text-gray-400">Max 500 characters. Provide a clear description of what this permission controls.</p>
              </div>

              {/* Module Name */}
              <div>
                <label htmlFor="module_name" className="block text-sm font-semibold text-purple-400 mb-1">
                  Module Name
                </label>
                <input
                  type="text"
                  id="module_name"
                  name="module_name"
                  className="w-full px-4 py-2 rounded-lg border border-gray-700 bg-black text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition"
                  value={formData.module_name}
                  onChange={handleInputChange}
                  maxLength={50}
                  placeholder="e.g., Users, Images, Reports (optional)"
                />
                <p className="mt-1 text-xs text-gray-400">Optional. Max 50 characters. Group related permissions by module.</p>
              </div>
            </div>

            {/* Submit Button Group */}
            <div className="flex justify-end pt-4 space-x-4">
              <button
                type="button"
                onClick={() => router.push('/PermissionsPage')}
                className="px-6 py-2 text-sm font-medium rounded-lg text-white bg-gray-800 border border-gray-600 hover:bg-gray-700 transition-all focus:ring-2 focus:ring-purple-500 focus:outline-none"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className={`px-6 py-2 text-sm font-medium rounded-lg text-white bg-gradient-to-r from-purple-600 to-purple-800 hover:from-purple-700 hover:to-purple-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 shadow-lg transition ${
                  loading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {loading ? 'Creating...' : 'Create Permission'}
              </button>
            </div>
          </form>
        </div>

        {/* Help Section */}
        <div className="mt-6 bg-gray-900 rounded-lg border border-gray-800 p-4">
          <h3 className="text-lg font-semibold text-purple-400 mb-2">Permission Guidelines</h3>
          <ul className="text-sm text-gray-300 space-y-1">
            <li>• Use clear, descriptive names that explain what the permission allows</li>
            <li>• Permission codes should be unique and use snake_case format</li>
            <li>• Group related permissions using the same module name</li>
            <li>• Common permission patterns: create_*, read_*, update_*, delete_*</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AddPermission;