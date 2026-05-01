# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0, 
    "Orlando": 0.85, 
    "Miami": 1.2, 
    "Jacksonville": 0.75, 
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9
    
    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday
    
    for store in stores:
        store_factor = store_performance[store]
        
        for dept in departments:
            dept_factor = dept_performance[dept]
            
            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)
                
                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise
                
                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range
                
                # Calculate profit
                profit = sales_amount * profit_margin
                
                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range
    
    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])
    
    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income
    
    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)
    
    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))
    
    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)
    
    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)
    
    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"
    
    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]
    
    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()
    
    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) * 
                                (store_performance[store] ** 0.5))
    
    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# TODO 1: Descriptive Analytics - Overview of Current Performance
# 1.1 Calculate and display basic descriptive statistics for sales and profit
# REQUIRED: Store results in variables for testing
def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    # Your code here
    total_sales = float(sales_df["Sales"].sum())
    total_profit = float(sales_df["Profit"].sum())
    avg_profit_margin = float(sales_df["ProfitMargin"].mean())
    sales_mean = float(sales_df["Sales"].mean())
    sales_median = float(sales_df["Sales"].median())
    sales_std = float(sales_df["Sales"].std())
    profit_mean = float(sales_df["Profit"].mean())
    profit_median = float(sales_df["Profit"].median())
    profit_std = float(sales_df["Profit"].std())
    sales_by_store = sales_df.groupby("Store")["Sales"].sum()
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum()


    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_profit_margin": avg_profit_margin,
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept}


# 1.2 Create visualizations showing sales distribution by store, department, and time
# REQUIRED: Return matplotlib figures
def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    # Your code here
    pass
    store_fig, ax1 = plt.subplots(figsize=(8,5))
    sales_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_store.plot(kind="bar", ax=ax1)
    ax1.set_title("Sales by Store")
    ax1.set_ylabel("Total Sales")
    dept_fig, ax2 = plt.subplots(figsize=(8,5))
    sales_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)
    sales_dept.plot(kind="bar", ax=ax2)
    ax2.set_title("Sales by Department")
    ax2.set_ylabel("Total Sales")
    time_fig, ax3 = plt.subplots(figsize=(10,5))
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.to_period("M"))["Sales"].sum()
    monthly_sales.index = monthly_sales.index.to_timestamp()
    monthly_sales.plot(kind="line", ax=ax3, marker='o')
    ax3.set_title("Monthly Sales Trend")
    ax3.set_ylabel("Total Sales")
   
    return (store_fig, dept_fig, time_fig)

# 1.3 Analyze customer segments and their spending patterns
# REQUIRED: Return analysis results
def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    # Your code here
    pass
    segment_counts=customer_df["Segment"].value_counts()
    segment_avg_spend=customer_df.groupby("Segment")["MonthlySpend"].mean()
    segment_loyalty=pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])
    
    return {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty
        }
        





# TODO 2: Diagnostic Analytics - Understanding Relationships
# 2.1 Identify factors correlated with sales performance
# REQUIRED: Return correlation results
def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    # Your code here
    pass
    corr_df=operational_df.select_dtypes(include=[np.number]).corr()
    if "AnnualSales" not in corr_df.columns:
        raise KeyError("AnnualSales not found in operational_df columns")
    corrs=corr_df['AnnualSales'].drop('AnnualSales').abs().sort_values(ascending=False)
    top_corrs=corrs.head(3)
    fig,ax= plt.subplots(figsize=(8,4))
    corr_df['AnnualSales'].drop('AnnualSales').plot(kind='bar', ax=ax, title='Correlations with Annual Sales')
    ax.set_ylabel('Pearson correlation')
    signed_top= [(f, float(corr_df.loc[f, 'AnnualSales'])) for f in top_corrs.index]


    return {
        "store_correlations": corr_df,
        "top_correlations": signed_top,
        "correlation_fig": fig
    }


# 2.2 Compare stores based on operational metrics
# REQUIRED: Return comparison results
def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    # Your code here
    pass
    efficiency_metrics=operational_df[["Store","SalesPerSqFt","SalesPerStaff"]].set_index("Store")
    performance_ranking= operational_df.set_index("Store")["AnnualProfit"].rank(ascending=False)
    fig,ax= plt.subplots(figsize=(9,5))
    operational_df.plot(x="Store", y=["SalesPerSqFt","SalesPerStaff"], kind="bar", ax=ax)
    ax.set_title("Store Efficiency: Sales per SqFt and Sales per Staff")
    
    return {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": fig
    }

# 2.3 Analyze seasonal patterns and their impact
# REQUIRED: Return seasonal analysis
def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    # Your code here
    pass
    monthly_sales= sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum()
    dow_sales= sales_df.groupby(sales_df["Date"].dt.dayofweek)["Sales"].mean()
    fig,(ax1, ax2)= plt.subplots(1,2,figsize=(12,4))
    monthly_sales.plot(kind="line", ax=ax1, marker='o')
    ax1.set_title("Monthly Total Sales")
    ax1.set_xlabel("Month")
    dow_sales.plot(kind="bar", ax=ax2)
    ax2.set_title("Average Sales by Day of Week (0=Mon)")
    ax2.set_xlabel("Day of Week")

    return {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": fig
    }



# TODO 3: Predictive Analytics - Basic Forecasting
# 3.1 Create a simple linear regression model to predict store sales
# REQUIRED: Return model results
def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    # Your code here
    pass
    x= store_df["SquareFootage"].values
    y= operational_df.set_index("Store").loc[store_df["Store"],"AnnualSales"].values
    slope,intercept= np.polyfit(x, y, 1)
    y_pred= intercept+ slope * x

    coefficients= {
        "SquareFootage": slope,
        "Intercept": intercept
    }

    ss_res= sum((y - y_pred) ** 2)
    ss_tot= sum((y - np.mean(y)) ** 2)
    r_squared= 1 - (ss_res / ss_tot)
    predictions= pd.Series(y_pred, index=store_df["Store"])
    fig, ax= plt.subplots(figsize=(6, 5))
    ax.scatter(x, y, label="Actual Sales")
    ax.plot(x, y_pred, color="red", label=f"Fit: Sales ≈ {intercept:.0f} + {slope:.2f}*SqFt")
    ax.set_xlabel("Square Footage")
    ax.set_ylabel("Annual Sales")
    ax.set_title("Store Sales Prediction")
    ax.legend()

    return {
        "coefficients": coefficients,
        "r_squared": float(r_squared),
        "predictions": predictions,
        "model_fig": fig
    }
  
    
# 3.2 Forecast departmental sales trends
# REQUIRED: Return forecast results
def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    # Your code here
    pass
    dept_trends= sales_df.groupby([sales_df["Date"].dt.to_period('M'),"Department"])["Sales"].sum().unstack(fill_value=0)
    dept_trends.index= dept_trends.index.to_timestamp()
    growth_rates= dept_trends.pct_change().mean().fillna(0)
    fig, ax= plt.subplots(figsize=(10,5))
    dept_trends.plot(ax=ax)
    ax.set_title("Department Monthly Sales Trends")

    return {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": fig
    }



# TODO 4: Integrated Analysis - Business Insights and Recommendations
# 4.1 Identify the most profitable combinations of store, department, and customer segments
# REQUIRED: Return opportunity analysis
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    # Your code here
    pass
    combo= sales_df.groupby(["Store","Department"])["Profit"].sum().reset_index()
    top= combo.sort_values("Profit", ascending=False).head(10)
    bottom= combo.sort_values("Profit", ascending=True).head(10)
    opp_score= combo.groupby("Store")["Profit"].sum().sort_values(ascending=False)

    return {
        "top_combinations": top,
        "underperforming": bottom,
        "opportunity_score": opp_score
    }

# 4.2 Develop recommendations for improving performance
# REQUIRED: Return list of recommendations
def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    # Your code here
    pass
    return [
        "Make the Miami store hours longer to make more off of the store because it is the top sales performer.",
        "Increase budgets for marketing for the Gainesville store to get more customer attention.",
        "Reduce staffing and inventory for January and February due to winter sales dipping.",
        "Schedule more staff members on the weekend due to increased sales on the weekend.",
        "Get stocked more on Prepared Foods and Produce in the summer when sales are at peak."
    ]


# TODO 5: Summary Report
# REQUIRED: Generate comprehensive summary
def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    # Your code here
    pass
    print("\nEXECUTIVE SUMMARY")
    print("Overview: GreenGrocer has five operating stores in Florida that has strong 2023 performances.")
    print("Miami leads in sales while Jacksonville and Gainseville struggle compared to it.")
    print("February is worst performing month for sales.")
    print("Produce and Prepared Foods are the most profitable departments.")
    print("Weekend sales are higher than weekday sales throughout all stores.")

    print("\nKey Findings:")
    print("- Miami is the top performing store while Gainesville is the lowest performing store.")
    print("- Sales peak in the summer and in December.")
    print("- Gaineville is the biggest store for square feet but the most underperforming store.")
    
    print("\nRecommendations:")
    for r in develop_recommendations():
        print(f"- {r}")

    print("\nExpected Impact:Extending store hours in Miami will raise sales and profits even more.")
    print("Increasing the Gainesville marketing will bring in more views and customers to their location.")
    print("Adding more staff for the weekend will improve sales and store efficiency.")
    print("Reducing staffing and inventory in January and February will help reduce costs during the slower seasons.")
    print("Stocking up on Prepared Foods and Produce in the summer will help maximize sales.")
    


# Main function to execute all analyses
# REQUIRED: Do not modify function name
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)
    
    # Execute analyses in a logical order
    # REQUIRED: Store all results for potential testing
    
    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()
    
    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()
    
    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()
    
    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()
    
    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()
    
    # Show all figures
    plt.show()
    
    # Return results for testing purposes
    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }

# Run the main function
if __name__ == "__main__":
    results = main()