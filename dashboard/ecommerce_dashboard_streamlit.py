import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.image as mpimg
import urllib.request

# Load data from cleaned dataframe
main_df = pd.read_csv('main_data_for_dashboard.csv')

# Define order_product_category function to return order_by_product_category_df
def order_product_category(df):
    order_by_product_category_df = df.groupby(by="product_category").agg(
        num_of_order=('order_id', 'count'),
        sum_order_value=('total_order_value', 'sum')
    ).reset_index()
    
    return order_by_product_category_df

# Load geolocation data
customers_silver = pd.read_csv("geolocation.csv")

# Plot function for Brazil map
def plot_brazil_map(data):
    brazil_img = mpimg.imread(urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'), 'jpg')
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(brazil_img, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
    ax.scatter(data["geolocation_lng"], data["geolocation_lat"], alpha=0.3, s=0.3, c='blue')
    ax.axis('off')
    st.pyplot(fig)

# Main Streamlit app
def main():
    # Title
    st.title("E-Commerce Dashboard")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Product Categories", "Customer Locations"])

    # Render selected page
    if page == "Product Categories":
        st.subheader("Product Categories")
        order_by_product_category_df = order_product_category(main_df)
        
        # Plot product categories with the most and least orders
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

        sns.barplot(
            x="num_of_order",
            y="product_category",
            data=order_by_product_category_df.sort_values(by=['num_of_order', 'sum_order_value'], ascending=False).head(10),
            palette="Blues_r",
            ax=ax[0]
        )
        ax[0].set_ylabel(None)
        ax[0].set_xlabel(None)
        ax[0].set_title("Most Ordered", loc="center", fontsize=15)
        ax[0].tick_params(axis='y', labelsize=12)

        sns.barplot(
            x="num_of_order",
            y="product_category",
            data=order_by_product_category_df.sort_values(by=['num_of_order', 'sum_order_value'], ascending=True).head(10),
            palette="Blues_r",
            ax=ax[1]
        )
        ax[1].set_ylabel(None)
        ax[1].set_xlabel(None)
        ax[1].invert_xaxis()
        ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[1].set_title("Least Ordered", loc="center", fontsize=15)
        ax[1].tick_params(axis='y', labelsize=12)
        plt.suptitle("Product Categories with Most and Least Orders", fontsize=20)
        st.pyplot(fig)

        # Plot product categories with the highest and lowest total order values
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

        sns.barplot(
            x="sum_order_value",
            y="product_category",
            data=order_by_product_category_df.sort_values(by='sum_order_value', ascending=False).head(10),
            palette="Reds_r",
            ax=ax[0]
        )
        ax[0].set_ylabel(None)
        ax[0].set_xlabel('Total Order Value', fontsize=12)
        ax[0].set_title("Highest Total Order Value", loc="center", fontsize=15)
        ax[0].tick_params(axis='y', labelsize=12)

        sns.barplot(
            x="sum_order_value",
            y="product_category",
            data=order_by_product_category_df.sort_values('sum_order_value', ascending=True).head(10),
            palette="Reds_r",
            ax=ax[1]
        )
        ax[1].set_ylabel(None)
        ax[1].set_xlabel('Total Order Value', fontsize=14)
        ax[1].invert_xaxis()
        ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[1].set_title("Lowest Total Order Value", loc="center", fontsize=17)
        ax[1].tick_params(axis='y', labelsize=12)
        plt.suptitle("Product Categories with Highest and Lowest Total Order Values", fontsize=20)
        st.pyplot(fig)

    elif page == "Customer Locations":
        st.subheader("Customer Locations in Brazil")
        plot_brazil_map(customers_silver.drop_duplicates(subset='customer_unique_id'))

if __name__ == "__main__":
    main()
