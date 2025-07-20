'use client';
import Image from 'next/image';
import Link from 'next/link';

const HRMWelcomeSection = () => {
  return (
    <section className="bg-gradient-to-br from-[#f8f9fa] via-[#eaeaea] to-[#f5f5f5] py-20 px-6">
      <div className="max-w-7xl mx-auto text-center">
        <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6 tracking-tight">
          Welcome to <span className="text-[#bfa054]">NextGen HR Management</span>
        </h1>
        <p className="text-gray-700 text-lg max-w-3xl mx-auto mb-12 leading-relaxed">
          Streamline your HR operations with a system designed for efficiency, security, and luxury. Experience the new era of workforce management.
        </p>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-10 mt-10">
          {[
            {
              icon: '/images/dashboard.png',
              title: 'Employee Dashboard',
              desc: 'Track attendance, leaves, and tasks with visual precision and ease.',
            },
            {
              icon: '/images/payroll.png',
              title: 'Automated Payroll',
              desc: 'Smart, compliant, and on-time salary solutions with built-in tax handling.',
            },
            {
              icon: '/images/performance.png',
              title: 'Performance Reviews',
              desc: 'Unlock insights to boost productivity and empower leadership.',
            },
          ].map((item, idx) => (
            <div
              key={idx}
              className="bg-white/70 backdrop-blur-md border border-gray-200 rounded-3xl p-8 shadow-lg hover:shadow-2xl transition duration-300 text-center"
            >
              <Image
                src={item.icon}
                alt={item.title}
                width={64}
                height={64}
                className="mx-auto mb-5"
              />
              <h3 className="text-2xl font-semibold text-gray-800">{item.title}</h3>
              <p className="text-sm text-gray-600 mt-3">{item.desc}</p>
            </div>
          ))}
        </div>

        {/* CTA Button */}
        <div className="mt-14">
          <Link
            href="/signup"
            className="inline-block bg-gradient-to-r from-[#bfa054] to-[#d4af37] text-white font-semibold px-8 py-4 rounded-full shadow-md hover:scale-105 hover:shadow-lg transition duration-300"
          >
            Get Started Now
          </Link>
        </div>
      </div>
    </section>
  );
};

export default HRMWelcomeSection;
