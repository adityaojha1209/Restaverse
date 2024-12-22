"use client";

import AuthSocialButton from "@/components/AuthSocialButton";
import { signIn, useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { BsGoogle } from "react-icons/bs";

const LoginPage = () => {
  const router = useRouter();
  const session = useSession();

  useEffect(() => {
    if (session?.status === "authenticated") router.push("/");
  }, [session, router]);

  const socialAction = async () => {
    signIn("google", {
      redirect: false,
    }).then((callback) => {
      console.log(callback);
    });
  };

  return (
    <div
      className="flex min-h-screen items-center justify-center bg-cover bg-center"
      style={{
        backgroundImage: `url('/background.jpg')`, // Path to your image in the public folder
      }}
    >
      <div className="sm:w-full sm:max-w-md w-full bg-gray-800 bg-opacity-70 border border-gray-700 rounded-lg shadow-lg p-8 space-y-6">
        <h2 className="text-4xl font-extrabold text-center text-white">
          Log in to Your Account
        </h2>
        <p className="text-center text-gray-400">
          Access your Google Business Profile
        </p>

        <div className="mt-8 flex justify-center gap-4">
          {/* Wrap AuthSocialButton with a div to apply custom styles */}
          <div className="w-full">
            <AuthSocialButton icon={BsGoogle} onClick={socialAction} />
          </div>
        </div>
        <div className="flex items-center justify-center"></div>
      </div>
    </div>
  );
};

export default LoginPage;
