'use client';
import Image from 'next/image';
import Link from 'next/link';

const WelcomeSection = () => {
  return (
    <>
      {/* Luxury Intro Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="bg-white/80 backdrop-blur-lg shadow-2xl rounded-3xl p-12 border border-gray-200">
          <h1 className="text-5xl md:text-6xl font-extrabold text-center text-gray-900 mb-6 tracking-tight">
            Welcome to <span className="text-[#bfa054]">Elite HR Management</span>
          </h1>
          <p className="text-lg text-center text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Empower your workforce with our elegant, modern HRM platform — built for performance, harmony, and excellence.
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-6 py-16 grid md:grid-cols-3 gap-12">
        {[
          {
            title: 'Smart Employee Dashboard',
            icon: '/images/dashboard.png',
          },
          {
            title: 'Performance Reviews',
            icon: '/images/performance.png',
          },
          {
            title: 'Automated Payroll',
            icon: '/images/payroll.png',
          },
        ].map((item, index) => (
          <div
            key={index}
            className="bg-white/70 backdrop-blur-xl border border-gray-200 rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300"
          >
            <Image
              src={item.icon}
              alt={item.title}
              width={64}
              height={64}
              className="mx-auto mb-5"
            />
            <h3 className="text-2xl font-semibold text-gray-800 text-center mb-3">
              {item.title}
            </h3>
            <p className="text-sm text-gray-500 text-center leading-relaxed">
              Streamline and elevate your operations with cutting-edge HR technology.
            </p>
          </div>
        ))}
      </section>

      {/* Call to Action */}
      <section className="bg-gradient-to-br from-[#1f1f1f] via-[#2d2d2d] to-[#3a3a3a] py-16 text-white text-center relative">
        <div className="max-w-4xl mx-auto px-6">
          <h2 className="text-4xl font-bold mb-4 tracking-tight">
            Ready to Modernize Your HR?
          </h2>
          <p className="mb-8 text-lg text-gray-300">
            Experience a luxurious approach to workforce management — secure, elegant, and powerful.
          </p>
          <Link
            href="/signup"
            className="inline-block bg-gradient-to-r from-[#bfa054] to-[#d4af37] text-white font-semibold py-3 px-8 rounded-full shadow-lg hover:scale-105 transition-transform duration-300"
          >
            Get Started
          </Link>
        </div>
      </section>
    </>
  );
};

export default WelcomeSection;
