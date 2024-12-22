"use client";
import ReviewCard from "@/components/ReviewCard";
import { reviewsType } from "@/type";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { Loader2, ServerCrash } from "lucide-react";

const DashboardPage = () => {
  const {
    data: reviews,
    isLoading,
    isError,
  } = useQuery<reviewsType[]>({
    queryKey: ["reviews"],
    queryFn: async () => {
      const response = await axios.get("http://127.0.0.1:8000/reviews/review");
      console.log(response.data);
      return response.data.reviews;
    },
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-full">
        <Loader2 className="animate-spin" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex justify-center items-center h-full flex-col space-y-2">
        <ServerCrash />
        <p>Somthing went wrong.</p>
      </div>
    );
  }

  return (
    <div>
      {reviews && reviews.length > 0 ? (
        <div className="flex justify-center items-center gap-2 flex-wrap my-6">
          {reviews.map((review) => {
            return (
              <ReviewCard
                key={review.reviewId}
                review={review}
              />
            );
          })}
        </div>
      ) : (
        <div className="my-6">
          <h1>No Reviews found</h1>
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
