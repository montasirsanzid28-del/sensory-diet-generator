from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database setup
DATABASE = 'sensory_diet.db'

def init_db():
    """Initialize the database with sample activities"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            min_age INTEGER NOT NULL,
            max_age INTEGER NOT NULL
        )
    ''')
    
    # Insert sample activities if table is empty
    cursor.execute('SELECT COUNT(*) FROM activities')
    if cursor.fetchone()[0] == 0:
        activities = [
            ('Deep Pressure Bear Hug', 'Calming', 'Child gives themselves a tight bear hug for 10-15 seconds', 3, 12),
            ('Wall Push-ups', 'Strengthening', 'Child does 10 push-ups against the wall', 4, 10),
            ('Heavy Work - Carry Books', 'Strengthening', 'Child carries a stack of books across the room', 3, 8),
            ('Jumping Jacks', 'Movement Break', 'Child does 10-15 jumping jacks', 4, 12),
            ('Simon Says', 'Movement Break', 'Play Simon Says with big movements', 3, 10),
            ('Deep Breathing', 'Calming', 'Child takes 5 slow deep breaths', 3, 12),
            ('Tight Squeeze', 'Calming', 'Child squeezes a stress ball or stuffed animal tightly', 3, 10),
            ('Chair Push-ups', 'Strengthening', 'Child does push-ups using a sturdy chair', 5, 12),
            ('Marching in Place', 'Movement Break', 'Child marches with high knees for 30 seconds', 3, 10),
            ('Tug-of-War', 'Strengthening', 'Child pulls gently on a resistance band or rope', 4, 12),
            ('Balloon Bop', 'Movement Break', 'Child keeps a balloon in the air using hands and feet', 3, 8),
            ('Weighted Blanket Time', 'Calming', 'Child sits under a weighted blanket for 5 minutes', 3, 10),
            ('Therapy Ball Wall Sits', 'Strengthening', 'Child sits against wall with therapy ball for 30 seconds', 4, 12),
            ('Finger Yoga', 'Movement Break', 'Child does finger stretches and hand exercises', 3, 10),
            ('Heavy Backpack Walk', 'Strengthening', 'Child walks around room with backpack filled with books', 5, 12),
            ('Calm Down Bottle', 'Calming', 'Child shakes and watches a homemade calm down bottle', 3, 8),
            ('Animal Walks', 'Movement Break', 'Child crawls like different animals (bear, crab, frog)', 3, 10),
            ('Resistance Band Pulls', 'Strengthening', 'Child pulls on resistance band 10 times', 5, 12),
            ('Deep Pressure Hand Squeeze', 'Calming', 'Child squeezes hands together tightly for 10 seconds', 3, 12),
            ('Balance Beam Walk', 'Movement Break', 'Child walks along taped line on floor', 4, 10),
            ('Sensory Bin Exploration', 'Calming', 'Child explores a bin filled with rice, beans, or sand', 3, 8),
            ('Hand-Eye Coordination Games', 'Movement Break', 'Child plays games like catch or bean bag toss', 4, 12),
            ('Therapy Putty Exercises', 'Strengthening', 'Child works with therapy putty for hand strengthening', 3, 10),
            ('Quiet Corner Time', 'Calming', 'Child spends time in a designated quiet space with calming items', 3, 12),
            ('Obstacle Course', 'Movement Break', 'Child navigates a simple obstacle course', 4, 10),
            ('Weighted Vest Walk', 'Strengthening', 'Child walks around room wearing a weighted vest', 5, 12),
            ('Fidget Tools Exploration', 'Calming', 'Child explores different fidget tools to find what helps them focus', 3, 12),
            ('Core Strengthening Planks', 'Strengthening', 'Child holds plank position for 15-30 seconds', 5, 12),
            ('Guided Visualization', 'Calming', 'Child listens to a calming guided visualization story', 3, 10),
            ('Crossing Midline Activities', 'Movement Break', 'Child reaches across body to touch opposite hand/foot', 4, 10),
            ('Tactile Exploration Box', 'Calming', 'Child explores different textures in a mystery box', 3, 8),
            ('Heavy Work Chair Pushes', 'Strengthening', 'Child pushes against a wall while sitting in a chair', 4, 10),
            ('Rhythm and Movement', 'Movement Break', 'Child follows rhythmic patterns with body movements', 3, 12),
            ('Hand Squeezes with Therapy Putty', 'Strengthening', 'Child squeezes therapy putty in different hand positions', 3, 10),
            ('Deep Pressure Rolling', 'Calming', 'Child rolls a foam roller over their arms and legs', 4, 12),
            ('Target Practice Games', 'Movement Break', 'Child throws balls or bean bags at targets', 4, 10),
            ('Wall Slides', 'Strengthening', 'Child slides down wall in sitting position and stands up', 5, 12),
            ('Sensory Story Time', 'Calming', 'Child listens to story while manipulating sensory items', 3, 8),
            ('Balance Challenges', 'Movement Break', 'Child practices standing on one foot or narrow surfaces', 4, 10),
            ('Hand Strengthening Squeezes', 'Strengthening', 'Child squeezes various resistance tools', 3, 12),
            ('Progressive Muscle Relaxation', 'Calming', 'Child tenses and relaxes different muscle groups', 5, 12),
            ('Motor Planning Obstacle Course', 'Movement Break', 'Child navigates course requiring planning and coordination', 4, 10),
            ('Finger Isolation Exercises', 'Strengthening', 'Child practices moving fingers independently', 3, 10),
            ('Weighted Lap Pad Time', 'Calming', 'Child sits with weighted lap pad during quiet activities', 3, 12),
            ('Cross-Crawl Exercises', 'Movement Break', 'Child touches opposite hand to knee in rhythmic pattern', 4, 10),
            ('Therapy Band Rows', 'Strengthening', 'Child pulls therapy band toward body while seated', 5, 12),
            ('Visual Tracking Games', 'Calming', 'Child follows moving objects with eyes only', 3, 8),
            ('Simon Says with Balance', 'Movement Break', 'Child follows commands while maintaining balance', 4, 10),
            ('Grip Strengthening Activities', 'Strengthening', 'Child practices different grip patterns with various objects', 3, 12)
        ]
        
        cursor.executemany('''
            INSERT INTO activities (name, category, description, min_age, max_age)
            VALUES (?, ?, ?, ?, ?)
        ''', activities)
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    """Homepage with description and disclaimer"""
    return render_template('home.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Form to collect child information and generate activities"""
    if request.method == 'POST':
        # Get form data
        child_name = request.form['child_name']
        age = int(request.form['age'])
        energy_level = request.form['energy_level']
        sensory_concern = request.form['sensory_concern']
        primary_goal = request.form['primary_goal']
        specific_needs = request.form['specific_needs']
        
        # Generate activities based on rules
        activities = get_suggested_activities(age, energy_level, sensory_concern, primary_goal)
        
        return render_template('results.html', 
                             child_name=child_name,
                             age=age,
                             energy_level=energy_level,
                             sensory_concern=sensory_concern,
                             primary_goal=primary_goal,
                             specific_needs=specific_needs,
                             activities=activities)
    
    return render_template('form.html')

def get_suggested_activities(age, energy_level, sensory_concern, primary_goal):
    """Generate suggested activities based on input criteria"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Determine activity categories based on rules
    categories = []
    
    if sensory_concern == 'Overstimulation' and energy_level == 'High':
        categories = ['Calming']
    elif sensory_concern == 'Low muscle tone':
        categories = ['Strengthening']
    elif sensory_concern == 'Attention issues':
        categories = ['Movement Break']
    elif sensory_concern == 'Sensory seeking':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory avoiding':
        categories = ['Calming']
    elif sensory_concern == 'Poor body awareness':
        categories = ['Strengthening', 'Movement Break']
    elif sensory_concern == 'Fine motor difficulties':
        categories = ['Strengthening']
    elif sensory_concern == 'Gross motor delays':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Tactile defensiveness':
        categories = ['Calming']
    elif sensory_concern == 'Vestibular processing issues':
        categories = ['Movement Break', 'Calming']
    elif sensory_concern == 'Proprioceptive seeking':
        categories = ['Strengthening']
    elif sensory_concern == 'Oral motor difficulties':
        categories = ['Strengthening']
    elif sensory_concern == 'Visual processing challenges':
        categories = ['Movement Break', 'Calming']
    elif sensory_concern == 'Auditory sensitivity':
        categories = ['Calming']
    elif sensory_concern == 'Motor planning difficulties':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory modulation disorder':
        categories = ['Calming', 'Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory discrimination disorder':
        categories = ['Movement Break', 'Calming']
    elif sensory_concern == 'Sensory-based motor disorder':
        categories = ['Strengthening', 'Movement Break']
    elif sensory_concern == 'Postural disorder':
        categories = ['Strengthening']
    elif sensory_concern == 'Dyspraxia':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory registration issues':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory sensitivity':
        categories = ['Calming']
    elif sensory_concern == 'Sensory defensiveness':
        categories = ['Calming']
    elif sensory_concern == 'Gravitational insecurity':
        categories = ['Movement Break', 'Calming']
    elif sensory_concern == 'Low registration':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory seeking behaviors':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory avoiding behaviors':
        categories = ['Calming']
    elif sensory_concern == 'Sensory over-responsivity':
        categories = ['Calming']
    elif sensory_concern == 'Sensory under-responsivity':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory craving':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory processing sensitivity':
        categories = ['Calming']
    elif sensory_concern == 'Sensory integration difficulties':
        categories = ['Movement Break', 'Strengthening']
    elif sensory_concern == 'Sensory processing challenges':
        categories = ['Movement Break', 'Calming', 'Strengthening']
    elif sensory_concern == 'Sensory processing differences':
        categories = ['Movement Break', 'Calming']
    elif sensory_concern == 'Sensory processing disorder':
        categories = ['Calming', 'Movement Break', 'Strengthening']
    else:
        # Default categories based on primary goal
        if primary_goal == 'Focus':
            categories = ['Movement Break', 'Calming']
        elif primary_goal == 'Calming':
            categories = ['Calming']
        elif primary_goal == 'Motor skills':
            categories = ['Strengthening', 'Movement Break']
        elif primary_goal == 'Sensory regulation':
            categories = ['Calming', 'Movement Break']
        elif primary_goal == 'Body awareness':
            categories = ['Strengthening', 'Movement Break']
        elif primary_goal == 'Coordination':
            categories = ['Movement Break', 'Strengthening']
        elif primary_goal == 'Strength building':
            categories = ['Strengthening']
        elif primary_goal == 'Balance improvement':
            categories = ['Movement Break', 'Strengthening']
        elif primary_goal == 'Fine motor development':
            categories = ['Strengthening']
        elif primary_goal == 'Gross motor development':
            categories = ['Movement Break', 'Strengthening']
        elif primary_goal == 'Attention span':
            categories = ['Movement Break', 'Calming']
        elif primary_goal == 'Emotional regulation':
            categories = ['Calming']
        elif primary_goal == 'Social interaction':
            categories = ['Movement Break']
        elif primary_goal == 'Self-confidence':
            categories = ['Movement Break', 'Strengthening']
    
    # Get activities from database
    placeholders = ','.join(['?' for _ in categories])
    query = f'''
        SELECT name, category, description
        FROM activities
        WHERE category IN ({placeholders})
        AND ? BETWEEN min_age AND max_age
        ORDER BY RANDOM()
        LIMIT 5
    '''
    
    cursor.execute(query, categories + [age])
    results = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    activities = [
        {
            'name': row[0],
            'category': row[1],
            'description': row[2]
        }
        for row in results
    ]
    
    return activities

if __name__ == '__main__':
    init_db()
    app.run(debug=True)