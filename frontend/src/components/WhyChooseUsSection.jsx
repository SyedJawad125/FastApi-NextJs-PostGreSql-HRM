'use client';
import Image from 'next/image';
import Link from 'next/link';

const WhyChooseUsSection = () => {
  return (
    <>
      {/* Why Choose Us Intro */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="bg-white/80 backdrop-blur-lg shadow-2xl rounded-3xl p-12 border border-gray-200 text-center">
          <h1 className="text-5xl font-extrabold text-gray-900 mb-6">
            Why <span className="text-[#bfa054]">Choose Us</span>
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Trusted by industry leaders, our HRM platform merges intuitive design with powerful features to transform your HR experience.
          </p>
        </div>
      </section>

      {/* Core Values Section */}
      <section className="max-w-7xl mx-auto px-6 py-16 grid md:grid-cols-3 gap-10">
        {[
          {
            icon: '/images/security.png',
            title: 'Data Security',
            desc: 'Enterprise-grade security to keep your workforce data safe and private.',
          },
          {
            icon: '/images/insight.png',
            title: 'Actionable Insights',
            desc: 'Gain data-driven clarity to support smarter HR decisions.',
          },
          {
            icon: '/images/support.png',
            title: '24/7 Support',
            desc: 'Elite customer care from a dedicated support team at any hour.',
          },
        ].map((item, i) => (
          <div
            key={i}
            className="bg-white/70 backdrop-blur-xl rounded-3xl p-8 shadow-lg border border-gray-200 text-center hover:shadow-2xl transition duration-300"
          >
            <Image
              src={item.icon}
              alt={item.title}
              width={60}
              height={60}
              className="mx-auto mb-5"
            />
            <h3 className="text-2xl font-semibold text-gray-800 mb-2">{item.title}</h3>
            <p className="text-gray-500 text-sm">{item.desc}</p>
          </div>
        ))}
      </section>

      {/* Stats Section */}
      <section className="bg-gradient-to-br from-[#1f1f1f] via-[#2a2a2a] to-[#3b3b3b] py-16 text-white text-center">
        <h2 className="text-3xl font-bold mb-8">Our Impact</h2>
        <div className="flex flex-wrap justify-center gap-12">
          {[
            { label: 'Companies Served', value: '1500+' },
            { label: 'Employees Managed', value: '85,000+' },
            { label: 'Avg. Satisfaction', value: '98%' },
          ].map((stat, idx) => (
            <div key={idx} className="flex flex-col items-center">
              <span className="text-4xl font-extrabold text-[#d4af37]">{stat.value}</span>
              <span className="text-gray-300 mt-1">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-white text-center">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Join the Future of HR</h2>
          <p className="text-gray-600 mb-8">
            Elevate your organization with intelligent HR management. Try it today — experience the difference.
          </p>
          <Link
            href="/signup"
            className="inline-block bg-gradient-to-r from-[#bfa054] to-[#d4af37] text-white font-semibold px-8 py-4 rounded-full shadow-lg hover:scale-105 transition duration-300"
          >
            Start Free Trial
          </Link>
        </div>
      </section>
    </>
  );
};

export default WhyChooseUsSection;
