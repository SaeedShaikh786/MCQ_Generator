if button and uploded_file is not None and mcq_count and subject and tone:
    with st.spinner("Loading..."):
        try:
            text = read_file(uploded_file)                    
            response = generate_evaluate_chain(
                {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                }
            )

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error")

        if isinstance(response, dict):

            # Extract the quiz data from response
            quiz = response.get('quiz', None)
            if quiz is not None:
                table_data = get_table_data(quiz)
            if table_data is not None:
                df = pd.DataFrame(table_data)
                df.index = df.index + 1
                st.table(df)
                # Display the review in the text box as well
                st.text_area(label="Review", value=response["review"])
            else:
                logging.info("Error in table Data")
                st.error("Error in the Table Data")

        else:
            st.write(response)
